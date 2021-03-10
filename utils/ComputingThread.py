import time
from threading import Thread

import cv2


class ComputingThread(Thread):

    def __init__(self, fps_fixer_thread, main_window):
        Thread.__init__(self)
        self.fps_fixer_thread = fps_fixer_thread
        self.main_window = main_window
        self.keep_going = True
        self.last_batch = []

    def run(self):

        while self.keep_going:

            if self.fps_fixer_thread.frame_1 is not None and self.fps_fixer_thread.frame_2 is not None:
                img_2, yolact_result = self.main_window.pipeline.process(self.fps_fixer_thread.frame_1, self.fps_fixer_thread.frame_2)
                self.last_batch = (img_2, yolact_result)

