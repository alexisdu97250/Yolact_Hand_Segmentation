from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui.MyOpenGLWidget import MyOpenGLWidget
import numpy as np


class OpenGLWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.opengl_widget = MyOpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)
        self.setWindowTitle("Test OpenGL")
        self.setGeometry(200, 200, 400, 400)

        keypoints = np.ones((21, 3))
        self.opengl_widget.receive_new_keypoints(keypoints)