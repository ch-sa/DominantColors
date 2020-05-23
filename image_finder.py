import pandas as pd
import numpy as np
from scipy.spatial import KDTree


class ImageFinder:

    def __init__(self, table_path):
        self.images, self.color_tree = read_table(table_path)

    def get_similar_images(self, color, n=10, min_area=0):
        print("Searching %s closest matches to selected color!" % n)
        rgb_color = np.array(hex2rgb(color))
        if min_area > 0:
            dist, points = self.color_tree.query(rgb_color, 2500)
        else:
            dist, points = self.color_tree.query(rgb_color, n)

        results = self.images.loc[points.tolist()]
        results["distance"] = np.round(dist, 2)
        results = results.sort_values(by=["distance", "count"], ascending=[True, False])

        if n > 0:
            results = results[results["count"] > min_area][:n]

        if len(results) > 0:
            print("Matching over, found %s images. Closest image is %s!" % (len(results),
                                                                            results.iloc[0][["meta_image"]]))
        return results


# HELPERS

# Reads in csv file and returns DataFrame
def read_table(path):
    images = pd.read_csv(path, index_col=0)
    print("Table has %s images with %s dominant colors from %s folders." %
          (len(images), len(images) * 4, len(images.meta_folder.unique())))

    np_colors = images[["red", "green", "blue"]].to_numpy()

    return images, KDTree(np_colors)


# Converts hex colors to rgb format (needs at at least 6 characters)
def hex2rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# Converts rgb colors to hex format
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex
