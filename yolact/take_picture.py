# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:15:44 2020

@author: abasel
"""
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
cap2= cv.videoCapture(0)
i=0
while(True):
    #Capture image par imaghe
    ret1, image1 = cap.read()
    ret2, image2 = cap2.read()
    
    
    
    if (ret1):
        cv.imshow("Cam 1", image1)
        if cv.waitKey(1) & 0xFF == ord('a'):
            cv.imwrite(r"C:\POC_Hand_Detection\datasets\stereo_hands\left\frame_"+str(i)+'.jpg',image1)
    if(ret2):
        cv.imshow("Cam 0", image2)
        if cv.waitKey(1) & 0xFF == ord('a'):
            cv.imwrite(r"C:\POC_Hand_Detection\datasets\stereo_hands\right\frame_"+str(i)+'.jpg',image2)
            i+=1
    elif cv.waitKey(1) & 0xFF == ord('q'):
        break
#Ne pas oublier de fermer le flux et la fenetre
cap.release()
cap2.release()
cv.destroyAllWindows()