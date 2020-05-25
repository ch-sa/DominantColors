# DominantColors
A graphical tool for retrieving images by dominating colors

![Screenshot of the image viewer](resources/ImageViewer_Screenshot.png)

## Main Steps
1. Select a folder (containing subfolders) with images
2. Extract the dominant colors & save them as index (*.csv)
3. Enter the color as hex or use the color picker
4. Find images dominated by that color

## Installation
The application is based on `pyqt 5.12` and clusters the images by color using `sklearn`. It was developed with `python 3.8` but any python version > 3 should be fine!

Simply clone this repository ...
```bash
git clone https://github.com/ch-sa/DominantColors.git
```

... and install the dependencies using `pip` or conda:
```bash
pip install -r requirements.txt
```

## Possible Future Features
- [ ] Improve index updating
- [ ] Also consider second & third dominant color
- [ ] Speed up index generation process
