import time
from threading import Thread

import cv2

from utils.ComputingThread import ComputingThread


class FpsFixerThread(Thread):

    def __init__(self, cap_1, cap_2, main_window):
        Thread.__init__(self)

        self.cap_1 = cap_1
        self.cap_2 = cap_2
        _, self.frame_1 = self.cap_1.read()
        _, self.frame_2 = self.cap_2.read()
        self.last_frame_was_at = time.time()
        self.main_window = main_window

        self.computing_thread = ComputingThread(self, main_window)
        self.computing_thread.start()

    def run(self):

        while self.cap_1.isOpened() and self.cap_2.isOpened():

            if time.time() > self.last_frame_was_at + 1.0 / 24:
                ret_1, self.frame_1 = self.cap_1.read()
                ret_2, self.frame_2 = self.cap_2.read()
                if ret_1 and ret_2:
                    self.last_frame_was_at = time.time()
                    if self.computing_thread.last_batch:
                        self.main_window.receiveBatch(self.computing_thread.last_batch[0], self.computing_thread.last_batch[1])
                else:
                    break


        self.computing_thread.keep_going = False
        self.computing_thread.join()
        self.cap_1.release()
        self.cap_2.release()
        raise ValueError("stopping execution...")
        


