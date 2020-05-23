import os
import pandas as pd
import numpy as np
import yaml

from PIL import Image, ImageFile
from datetime import datetime

ImageFile.LOAD_TRUNCATED_IMAGES = True
from sklearn.cluster import KMeans
from collections import Counter


class IndexGenerator:

    def __init__(self, index_gui, controler):
        self.index_gui = index_gui
        self.nxt_control = controler
        self.image_folder = ""
        self.index_path = ""

        # CONFIG
        self.SILENT = True
        self.WIDTH = 128
        self.HEIGHT = 128
        self.CLUSTERS = 6  # number of extracted colors

        self.connect_events()

    def connect_events(self):
        self.index_gui.makeButton.clicked.connect(self.generate_index)
        self.index_gui.continueButton.clicked.connect(self.set_index)

    def log(self, text):
        self.index_gui.showLog(text)

    def generate_index(self):
        self.index_gui.makeButton.setEnabled(False)

        self.image_folder = self.index_gui.folderLineEdit.text()
        self.index_path = self.index_gui.indexLineEdit.text()

        self.log("Searching %s for images (*.jpg, *.jpeg & *.png supported) ..." % self.image_folder)

        # Find all images recursive
        image_paths = []

        for dirpath, dirnames, filenames in os.walk(self.image_folder):
            for filename in [f for f in filenames if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")]:
                image_paths.append(os.path.join(dirpath, filename))

        self.log("Found %s images!" % len(image_paths))

        self.extract_colors(sorted(image_paths))

    def extract_colors(self, image_paths):
        # OLD FORMATING
        # columns=["image", "color_1", "count_1", "color_2", "count_2",
        #          "color_3", "count_3", "color_4", "count_4", "parent_folder", "path"])

        df_columns = ["meta_image", "meta_path", "meta_folder", "red", "green", "blue", "count"]
        dom_colors = pd.DataFrame(columns=df_columns)

        no_of_images = len(image_paths)
        self.log("Starting color extraction process ...")

        for ind, image_path in enumerate(image_paths):

            try:
                # Get image name and parent folder
                image_name = os.path.basename(image_path)
                parent_folder = os.path.split(os.path.split(image_path)[0])[1]

                # Load image
                image = Image.open(image_path)
                if not self.SILENT:
                    self.log("Loaded {f} image {n}. Size: {s:.2f} KB. Dimensions: ({d})".format(
                        f=image.format, n=image_name, s=os.path.getsize(image_path) / 1024, d=image.size))

                # Transform image
                new_width, new_height = calculate_new_size(image, self.WIDTH, self.HEIGHT)
                image = image.resize((new_width, new_height), Image.ANTIALIAS)

                img_array = np.array(image)
                img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))

                # Modeling
                model = KMeans(n_clusters=self.CLUSTERS)
                labels = model.fit_predict(img_vector)
                label_counts = Counter(labels)

                hex_colors = [rgb2hex(center) for center in model.cluster_centers_]

                results = list(zip(hex_colors, list(label_counts.values())))
                results.sort(key=lambda tup: tup[1], reverse=True)

                print(results)

                hex_color, count = results[0]
                rgb_colors = hex2rgb(hex_color)

                print("Col: %s,\t Count: %s" % (rgb_colors, count))

                dom_colors.loc[len(dom_colors)] = [image_name, image_path, parent_folder] + rgb_colors + [count]

                if not self.SILENT:
                    print("Dominating color is: %s with %s counts" % results[0])

                progress = round((ind + 1) / no_of_images * 100)
                self.index_gui.indexProgressBar.setValue(progress)

                # Make subsequent backup
                # if (ind+1) % 500 == 0:
                #    dom_colors.to_csv(os.path.join("AllImages", "allimagesDom-3_" + str(f"{ind+1:04d}") + ".csv"))

            except:
                self.log("Error occured at with image no. %s (%s in %s)" % (ind, image_name, parent_folder))

        dom_colors.to_csv(self.index_path)
        print("Saved dominant colors of %s images in %s" % (len(dom_colors), self.index_path))
        self.log("Saved dominant colors of %s images in %s" % (len(dom_colors), self.index_path))
        self.log("Could extract colors from %s of %s images (%s %%)" % (len(dom_colors), no_of_images,
                                                                        round(len(dom_colors) * 100 / no_of_images)))

        self.index_gui.continueButton.setVisible(True)
        self.index_gui.makeButton.setEnabled(True)

    def set_index(self):
        save_path_to_config(self.index_path)
        self.nxt_control.load_index_path()
        self.index_gui.accept()


# HELPER FUNCTIONS
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex


def hex2rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def calculate_new_size(image, WIDTH, HEIGHT):
    if image.width >= image.height:
        wpercent = (WIDTH / float(image.width))
        hsize = int((float(image.height) * float(wpercent)))
        new_width, new_height = WIDTH, hsize
    else:
        hpercent = (HEIGHT / float(image.height))
        wsize = int((float(image.width) * float(hpercent)))
        new_width, new_height = wsize, HEIGHT
    return new_width, new_height


def save_path_to_config(index_path):
    config = yaml.safe_load(open("../config.yml"))
    config["image_viewer"]["index_path"] = index_path
    config["color_index_creator"]["last_created"] = str(datetime.now())
    with open("../config.yml", 'w') as file:
        yaml.dump(config, file)
