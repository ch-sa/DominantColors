from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView


# TODO fix point size error

class Gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        uic.loadUi('resources/UserInterfaces/mainwindow.ui', self)
        self.setWindowIcon(QtGui.QIcon("resources/Icons/Palette-Icon_window.ico"))

        # Color selection
        self.colorShower = self.findChild(QtWidgets.QLabel, "colorShower")
        self.colorButton = self.findChild(QtWidgets.QPushButton, "colorPicker")
        self.hexInput = self.findChild(QtWidgets.QLineEdit, "hexColor")

        # Image search
        self.imageFilterCB = self.findChild(QtWidgets.QCheckBox, "checkBox")
        self.searchButton = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.progressBar = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progressBar.hide()

        # Advanced settings
        self.dialFrame = self.findChild(QtWidgets.QFrame, "frame_2")

        self.dialImgNo = self.findChild(QtWidgets.QDial, "dialImgNo")
        self.lineEditImgNo = self.findChild(QtWidgets.QLineEdit, "lineEditImageNo")

        self.dialArea = self.findChild(QtWidgets.QDial, "dialArea")
        self.lineEditArea = self.findChild(QtWidgets.QLineEdit, "lineEditArea")

        self.dialFrame.hide()

        self.buttonFrame = self.findChild(QtWidgets.QFrame, "frame_3")

        self.changeIndexButton = self.findChild(QtWidgets.QPushButton, "changeButton")
        self.generateIndexButton = self.findChild(QtWidgets.QPushButton, "generateButton")

        self.buttonFrame.hide()

        # Output
        self.textOutput = self.findChild(QtWidgets.QLabel, "textOutput")

        # Image gallery
        self.imageGallery = self.findChild(QWebEngineView, "imageGallery")

        self.show()
