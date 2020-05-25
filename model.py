import bs4

from image_finder import ImageFinder


class Model:

    def __init__(self):
        self.website_template = "resources/Website/index_template.html"
        self.website_path = "resources/Website/index.html"
        self.table_path = None  #"resources/data/images-doc.csv"
        self.image_finder = None
        self.matched_table = None

    def set_index_path(self, path):
        self.table_path = path
        self.image_finder = ImageFinder(self.table_path)
        print("Color index was (re-)set to %s!" % self.table_path)

    def match_images(self, color, img_no, min_area):
        self.matched_table = self.image_finder.get_similar_images(color, img_no, min_area)
        if len(self.matched_table) == 0:
            print("Did not find any matching image to given criteria!")
            return False
        else:
            return True

    def update_website(self):
        print("Preparing %s images ..." % len(self.matched_table))
        image_paths = self.matched_table.meta_path.values

        # load the file
        with open(self.website_template) as website:
            html = website.read()
            site = bs4.BeautifulSoup(html, features="html.parser")

        for img in image_paths:
            # create new image box
            att_div1 = {'class': "gallery-item"}
            att_div2 = {'class': "content"}
            new_image_box = site.new_tag("div", **att_div1)
            div2 = site.new_tag("div", **att_div2)
            img = site.new_tag("img", src=img, alt=img)

            div2.append(img)
            new_image_box.append(div2)
            site.find("div", id="gallery").append(new_image_box)

        # <div class="gallery-item">
        #    <div class="content"><img src="https://source.unsplash.com/random/?tech,card" alt=""></div>
        # </div>

        # save the file again
        with open(self.website_path, "w") as outgoing_file:
            outgoing_file.write(str(site))
