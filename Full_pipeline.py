import time

import cv2
import cv2 as cv
from yolact.real_time_yolact import Real_time_yolact
import numpy as np


class Full_pipeline():


    def __init__(self):
        self.yolact_cnn = Real_time_yolact()
        # self.disparity_entity = Real_time_disparity()
        # self.V2V_PoseNet = V2V_PoseNet_outputs_QT()

        self.doSegmentation = True


    def process(self, img_1, img_2 = None):

        if self.doSegmentation:
            mask_2 = self.yolact_cnn.process(img_1, img_2)

            if not np.count_nonzero(mask_2):
                yolact_result = mask_2
                keypoints = np.ones((21, 3))
                disparity_map = mask_2
                return img_2, yolact_result


            # if self.doSegmentation:
            #     disparity_map = cv.bitwise_and(disparity_map, disparity_map, mask=mask_2)
            # disparity_map[disparity_map != 0] -= np.min(disparity_map)
            # disparity_map[disparity_map <= self.V2V_PoseNet.min_depth] = 0

        # else:
        #     disparity_map = np.zeros((20, 20))



        #keypoints = np.ones((21, 3))

        if self.doSegmentation:
            yolact_result = cv.bitwise_and(img_2, img_2, mask=mask_2)
        else:
            yolact_result = np.zeros((img_2.shape[0], img_2.shape[1], img_2.shape[2]))


        return img_2, yolact_result
