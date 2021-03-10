import time

import cv2
from PyQt5 import QtWidgets
from gui.Ui_MainWindow import Ui_MainWindow
from Full_pipeline import Full_pipeline
import sys

if __name__ == "__main__":
    fullPipeline = Full_pipeline()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, fullPipeline)

    MainWindow.show()

    sys.exit(app.exec_())
