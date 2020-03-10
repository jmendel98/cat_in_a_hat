import cv2
import numpy as np
import math
import re
from matplotlib import pyplot as plt

def distance_calculator (img):
    output = img.copy()
    measured_radius = 0.262 #in feet
    field_of_view = 1.22 #in radians
    horizontal_pixels = 1280 #width of screen in camera

    

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    distance_to_target = 0;

    # param2: accumulator threshold - the higher it is, the less circles you get,
    # and these circles have a higher probability of being correct. Best value is different
    # for every image (https://stackoverflow.com/questions/10716464/what-are-the-correct-usage-parameter-values-for-houghcircles-in-opencv-for-iris)
    # 4th parameter: min distance between center of detected circles.
    # Setting to large number so we only get the best one
    # explanation of parameters: https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
    # fine tuning parameters: https://stackoverflow.com/questions/26254287/houghcircles-circle-detection-using-opencv-and-python
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 9999, param2=50, minRadius=1, maxRadius=100)
    # while circles.size() is not 1:

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # do calculation with diameter (2*r) to figure out distance of circle from camera
            angle_of_target = ((2*r)/horizontal_pixels)*field_of_view #70 degree field of view angle(in radians)
            distance_to_target = measured_radius/math.tan(angle_of_target) #distance calculator

            h, w, _ = img.shape
            print("%d",distance_to_target)
            cv2.putText(output, "%d pixels wide circle." % (2*r), (w - 150, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 255], 2)

        # show the output image
        cv2.imshow("output", np.hstack([img, output]))
        cv2.waitKey(1)
    return distance_to_target
    
cam = cv2.VideoCapture(0)
    
while 1:
    key_pressed = input('Press ENTER to continue:') #tries to take a picture when prompted
    print(key_pressed)
    _, img = cam.read()
    distance =  distance_calculator(img)
    print("%d",distance)
    
