# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 04:16:55 2021

@author: basel
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_qt.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog

from gui.MyOpenGLWidget import MyOpenGLWidget
from gui.fileedit import FileEdit
from PIL.ImageQt import ImageQt
import numpy as np
from Full_pipeline import Full_pipeline
from utils.ComputingThread import ComputingThread
from utils.FpsFixerThread import FpsFixerThread


class Ui_MainWindow(object):

    def setupUi(self, MainWindow, fullPipeline):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("DWYH - Drive With Your Hand")
        MainWindow.resize(920, 770)
        self.mainWindow = MainWindow
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 20, 371, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        #self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        #self.pushButton.setGeometry(QtCore.QRect(420, 20, 75, 23))
        #self.pushButton.setObjectName("pushButton")
        self.openGLWidget = MyOpenGLWidget(self.centralWidget)
        self.openGLWidget.setGeometry(QtCore.QRect(510, 400, 371, 311))
        self.openGLWidget.setObjectName("openGLWidget")
        self.widget = QtWidgets.QLabel(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(30, 60, 371, 311))
        self.widget.setObjectName("widget")
        self.checkBox = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox.setGeometry(QtCore.QRect(670, 10, 81, 41))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setChecked(True)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_2.setGeometry(QtCore.QRect(520, 10, 91, 41))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setChecked(True)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_3.setGeometry(QtCore.QRect(820, 10, 81, 41))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setChecked(True)
        self.widget_2 = QtWidgets.QLabel(self.centralWidget)
        self.widget_2.setGeometry(QtCore.QRect(30, 400, 371, 311))
        self.widget_2.setObjectName("widget_2")
        self.widget_3 = QtWidgets.QLabel(self.centralWidget)
        self.widget_3.setGeometry(QtCore.QRect(510, 60, 371, 311))
        self.widget_3.setObjectName("widget_3")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(190, 370, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(670, 370, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(200, 710, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(690, 710, 81, 16))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(30, 0, 81, 16))
        self.label_5.setObjectName("label_5")

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1256, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.connectButtons()
        self.pipeline = fullPipeline
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.receiveBatch(np.zeros((20, 20, 3)), np.zeros((20, 20, 3)), np.zeros((20, 20)), np.ones((21, 3)))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DWYH - Drive With Your Hand"))
        self.comboBox.setItemText(0, _translate("MainWindow", " "))
        self.comboBox.setItemText(1, _translate("MainWindow", "webcam"))
        self.comboBox.setItemText(2, _translate("MainWindow", "image file"))
        self.comboBox.setItemText(3, _translate("MainWindow", "video file"))
        #self.pushButton.setText(_translate("MainWindow", "Start"))
        self.checkBox.setText(_translate("MainWindow", "Segmentation"))
        self.label.setText(_translate("MainWindow", "Data In"))
        self.label.setText(_translate("MainWindow", "Segmentation"))
        self.label_5.setText(_translate("MainWindow", "Data Source"))

    def handleComboBox(self):
        if self.comboBox.currentText() == "video file":
            self.openGLWidget.rotate = False
            _, video_1_path = self.getfiles("RIGHT CAMERA FILE")
            cap_1 = cv2.VideoCapture(video_1_path)
            cap_2 = cap_1

            fps_fixer_thread = FpsFixerThread(cap_1, cap_2, self)
            fps_fixer_thread.start()

        if self.comboBox.currentText() == "image file":

            self.openGLWidget.rotate = True
            _, img_1_path = self.getfiles("RIGHT CAMERA FILE")
            img_1 = cv2.imread(img_1_path)

            if self.pipeline.doDepth :
                _, img_2_path = self.getfiles("LEFT CAMERA FILE")
                img_2 = cv2.imread(img_2_path)
            else:
                img_2 = img_1

            self.video = False

            img_2, yolact_result, disparity_map, keypoints = self.pipeline.process(img_1, img_2)
            self.receiveBatch(img_2, yolact_result, disparity_map, keypoints)

        if self.comboBox.currentText() == "dataset":
            file = self.getfiles()
            self.video = False

        if self.comboBox.currentText() == "webcam":

            self.openGLWidget.rotate = False
            self.video = True
            cap_1 = cv2.VideoCapture(0)
            cap_2=cap_1

            fps_fixer_thread = FpsFixerThread(cap_1, cap_2, self)
            fps_fixer_thread.start()

    def switchSegmentation(self, new_mode):
        self.pipeline.doSegmentation = new_mode


    def connectButtons(self):
        self.comboBox.activated.connect(self.handleComboBox)
        self.checkBox_2.stateChanged.connect(self.switchSegmentation)
        self.checkBox.stateChanged.connect(self.switchDepth)
        self.checkBox_3.stateChanged.connect(self.switchSkeletton)


    def receiveBatch(self, source, yolact, disparity, keypoints):
        self.openGLWidget.receive_new_keypoints(keypoints)
        self.widget.setPixmap(self.adaptColouredSourceImage(source))
        self.widget_3.setPixmap(self.adaptColouredSourceImage(yolact))
        self.widget_2.setPixmap(self.adaptGraySourceImage(disparity))

    def adaptColouredSourceImage(self, image):

        image = image.astype('uint8')
        image = cv2.resize(image, (371, 311))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(image)

    def adaptGraySourceImage(self, image):

        image = image.astype('uint8')

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        return self.adaptColouredSourceImage(image)

    def getfiles(self, title="open"):
        dlg = QFileDialog(self.mainWindow)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle(title)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                return f, filenames[0]
