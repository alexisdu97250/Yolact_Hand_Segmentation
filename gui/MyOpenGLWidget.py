from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *
import numpy as np


class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
        theta = np.pi / 96
        self.rotation = [[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]]
        self.rotate = True
        self.keypoints = np.ones((21, 3))
        self.normalizeKeypoints()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_COLOR_MATERIAL)

    def paintGL(self):
        glMatrixMode(GL_PROJECTION)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.paintFingers()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def normalizeKeypoints(self):

        mins = [np.min(self.keypoints[:, 0]), np.min(self.keypoints[:, 1]), np.min(self.keypoints[:, 2])]

        self.keypoints = np.subtract(self.keypoints, mins)

        max = np.max(self.keypoints)

        if np.count_nonzero(self.keypoints):
            self.keypoints = np.divide(self.keypoints, max)

        self.keypoints = np.subtract(self.keypoints, [0.5, 0.5, 0.5])


    def paintFingers(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)
        padding = 0.01

        white = (1.0, 1.0, 1.0)
        red = (1.0, 0.0, 0.0)
        blue = (0.0, 0.0, 1.0)
        green = (0.0, 1.0, 0.0)
        yellow = (1.0, 1.0, 0.0)

        if np.all(self.keypoints == -0.5):
            return

        if self.rotate:
            self.keypoints = np.asarray([self.keypoints[i].dot(self.rotation) for i in range(21)])
        else:
            self.keypoints = np.asarray(self.keypoints)


        colors = [red, blue, green, yellow, white]

        color = white
        keypoint = self.keypoints[0]
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_QUADS)
        glVertex3f(keypoint[0] - padding, keypoint[1] - padding, keypoint[2])
        glVertex3f(keypoint[0] + padding, keypoint[1] - padding, keypoint[2])
        glVertex3f(keypoint[0] + padding, keypoint[1] + padding, keypoint[2])
        glVertex3f(keypoint[0] - padding, keypoint[1] + padding, keypoint[2])
        glEnd()

        for i in range(1, 21):
            color = colors[int((i - 1) / 4)]
            glColor3f(color[0], color[1], color[2])
            keypoint = self.keypoints[i]
            glBegin(GL_QUADS)
            glVertex3f(keypoint[0] - padding, keypoint[1] - padding, keypoint[2])
            glVertex3f(keypoint[0] + padding, keypoint[1] - padding, keypoint[2])
            glVertex3f(keypoint[0] + padding, keypoint[1] + padding, keypoint[2])
            glVertex3f(keypoint[0] - padding, keypoint[1] + padding, keypoint[2])
            glEnd()

        for finger in range(5):

            color = colors[finger]
            glColor3f(color[0], color[1], color[2])

            glBegin(GL_LINES)
            glVertex3f(self.keypoints[finger * 4 + 1][0], self.keypoints[finger * 4 + 1][1],
                       self.keypoints[finger * 4 + 1][2])
            glVertex3f(self.keypoints[0][0], self.keypoints[0][1], self.keypoints[0][2])
            glEnd()

            for part in range(3):
                glBegin(GL_LINES)
                glVertex3f(self.keypoints[finger * 4 + 1 + part][0], self.keypoints[finger * 4 + 1 + part][1],
                           self.keypoints[finger * 4 + 1 + part][2])
                glVertex3f(self.keypoints[finger * 4 + 2 + part][0], self.keypoints[finger * 4 + 2 + part][1],
                           self.keypoints[finger * 4 + 2 + part][2])
                glEnd()

    def receive_new_keypoints(self, new_keypoints):
        self.keypoints = new_keypoints
        self.normalizeKeypoints()
