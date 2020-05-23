import bs4

from image_finder import ImageFinder


class Model:

    def __init__(self):
        self.website_template = "resources/Website/index_template.html"
        self.website_path = "resources/Website/index.html"
        self.table_path = None  #"resources/data/images-doc.csv"
        self.image_finder = None

    def set_index_path(self, path):
        self.table_path = path
        self.image_finder = ImageFinder(self.table_path)

    def match_images(self, color, img_no, min_area):
        self.matched_table = self.image_finder.get_similar_images(color, img_no, min_area)
        if len(self.matched_table) == 0:
            print("Did not find any matching image to given criteria!")
            return False
        else:
            return True

    def prepare_images(self):
        print("Preparing %s images ..." % len(self.matched_table))
        self.images = self.matched_table.meta_path.values

    def update_website(self):
        # load the file
        with open(self.website_template) as webfile:
            html = webfile.read()
            site = bs4.BeautifulSoup(html, features="html.parser")

        for img in self.images:
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
        with open(self.website_path, "w") as outf:
            outf.write(str(site))
