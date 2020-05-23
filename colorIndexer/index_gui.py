from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog


class IndexGui(QtWidgets.QDialog):
    def __init__(self):
        super(IndexGui, self).__init__()
        uic.loadUi('resources/UserInterfaces/generateindex.ui', self)
        self.setWindowIcon(QtGui.QIcon("../resources/Icons/Palette-Icon_window.ico"))

        # Image folder selection
        self.folderButton = self.findChild(QtWidgets.QPushButton, "folderSelector")
        self.folderLineEdit = self.findChild(QtWidgets.QLineEdit, "folderPathEdit")
        self.recursiveCheckBox = self.findChild(QtWidgets.QCheckBox, "recursiveCheckBox")

        # Index storage
        self.indexButton = self.findChild(QtWidgets.QPushButton, "indexSelector")
        self.indexLineEdit = self.findChild(QtWidgets.QLineEdit, "indexPathEdit")

        # Index generation
        self.indexProgressBar = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.indexLogBrowser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")

        self.makeButton = self.findChild(QtWidgets.QPushButton, "makeIndexButton")
        self.continueButton = self.findChild(QtWidgets.QPushButton, "continueButton")
        self.continueButton.setVisible(False)
        self.chancelButton = self.findChild(QtWidgets.QPushButton, "chancelButton")

        self.connectToEvents()
        self.show()

    def connectToEvents(self):
        self.folderButton.clicked.connect(self.selectImageFolder)
        self.indexButton.clicked.connect(self.selectIndexPath)

    # File location selection
    def selectImageFolder(self):
        self.folderLineEdit.setText(QFileDialog().getExistingDirectory(self, 'Select directory',
                                                                       options=QFileDialog.DontUseNativeDialog))

    def selectIndexPath(self):
        save_path, ending = QFileDialog.getSaveFileName(self, 'Location for Generated Index File', '',
                                                filter='*.csv', options=QFileDialog.DontUseNativeDialog)

        if save_path[-4:] != ".csv":
            save_path += ending
        self.indexLineEdit.setText(save_path)

    def showLog(self, text):
        self.indexLogBrowser.append(text)
        self.indexLogBrowser.show()
