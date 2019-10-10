# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 19:01:06 2019

@author: kkapr
"""

import cv2

webcam = cv2.VideoCapture(0)
for num_pics in range(5):
    return_value, image = webcam.read()
    cv2.imwrite('mywebcam_pic'+str(num_pics)+'.png', image)
del(webcam)