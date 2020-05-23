import yaml
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog

from gui import Gui
from model import Model


class Control:

    def __init__(self, model: Model, view: Gui):
        self.model = model
        self.view = view

        self.connect_events()

    def connect_events(self):
        # Color selection
        self.view.colorButton.colorChanged.connect(self.onColorChanged)

        # Input checkup
        self.view.searchButton.clicked.connect(self.check_color_input)

        # Image search and presentation
        self.view.imageGallery.loadProgress.connect(self.loadProgressHandler)

        # Advanced settings
        self.view.imageFilterCB.stateChanged.connect(self.advancedSettings)

        self.view.dialImgNo.valueChanged.connect(lambda x: self.view.lineEditImgNo.setText(str(x)))
        self.view.lineEditImgNo.textChanged.connect(lambda x: self.view.dialImgNo.setValue(int(x)))

        self.view.dialArea.valueChanged.connect(lambda x: self.view.lineEditArea.setText(str(x)))
        self.view.lineEditArea.textChanged.connect(lambda x: self.view.dialArea.setValue(int(x)))

        self.view.changeIndexButton.clicked.connect(self.change_index_path)

    # EVENTS
    def load_index_path(self):
        config = yaml.safe_load(open("config.yml"))
        index_path = config["image_viewer"].get("index_path")
        self.model.set_index_path(index_path)

    def change_index_path(self):
        index_path = QFileDialog.getOpenFileName(QFileDialog(), "Select a Generated Index File",
                                                 os.getcwd(), "csv(*.csv)", options=QFileDialog.DontUseNativeDialog)[0]
        self.model.set_index_path(index_path)

    def onColorChanged(self):
        print("Color has been changed!")
        tmp_color = self.view.colorButton.color()
        self.view.hexInput.setText(tmp_color)
        self.show_color_circle(tmp_color)

    def show_color_circle(self, color: str):
        self.view.colorShower.setStyleSheet("QLabel {font-size: 60px; color: " + color + "; }")

    # Check the correctness of the user input for the color
    def check_color_input(self):
        self.view.textOutput.clear()
        error_msg = "Please enter a valid color in hex-format (#123456)."
        selected_color = self.view.hexInput.text()

        # Sanity Check
        if len(selected_color) == 4:
            selected_color = "#" + selected_color[1] * 2 + selected_color[2] * 2 + selected_color[3] * 2
            self.view.hexInput.setText(selected_color)
        elif len(selected_color) < 6:
            self.view.textOutput.setText(error_msg)
            return

        print('Selected color:' + selected_color)
        self.show_color_circle(selected_color)
        self.prepare_website(selected_color)

    def prepare_website(self, selected_color: str):
        self.view.progressBar.show()

        # Matching images
        no_of_images = self.view.dialImgNo.value()
        min_area = self.view.dialArea.value()
        success = self.model.match_images(selected_color, no_of_images, min_area)
        if not success:
            error_msg = "Did not find any matching image to the given criteria!" \
                        " Please adapt your settings and retry. :)"
            self.view.textOutput.setText(error_msg)
            return

        # Preparing images
        print("Preparing images ...")
        self.model.prepare_images()

        # Update website
        print("Prepare website ...")
        self.model.update_website()

        # Publish website
        print("Publishing website")
        self.view.imageGallery.page().profile().clearHttpCache()
        site_url = QUrl("file:///" + os.path.join(os.getcwd(), "resources/Website/index.html"))
        self.view.imageGallery.load(site_url)

    def loadProgressHandler(self, progress: int):
        self.view.progressBar.setValue(progress)

    def advancedSettings(self, activated: bool):
        self.view.dialFrame.setVisible(activated)
        self.view.buttonFrame.setVisible(activated)
