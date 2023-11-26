import sys
import yaml

from pathlib import Path

from PyQt5 import QtWidgets

from control import Control
from gui import Gui
from colorIndexer.index_generator import IndexGenerator
from colorIndexer.index_gui import IndexGui
from model import Model

app = QtWidgets.QApplication(sys.argv)

# Loading Config
config = yaml.safe_load(open("config.yml"))

INDEX_PATH = config["image_viewer"].get("index_path")
INDEX_DATE = config["color_index_creator"].get("last_created")
print(INDEX_PATH)

# Load GUI
window = Gui()
model = Model()
control = Control(model, window)

if INDEX_PATH is None or not Path(INDEX_PATH).exists():
    print("Don't have index file. Starting index generator ...")
    index_gui = IndexGui()
    index_generator = IndexGenerator(index_gui, control)
else:
    control.load_index_path()

# Execute application
app.exec()
