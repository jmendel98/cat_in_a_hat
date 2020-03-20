import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
import cv2
import numpy as np
import math
import re
from matplotlib import pyplot as plt

server_ip = "192.168.43.104"

#TOPICS LIST
player_input = "player input"
button_push = "button push"
game_update_location = "game update/position"
start_recognition = "start recognition"
recognition_results = "recognition results"

def button_prompt():
    time.sleep(2)
    publish.single(button_push, " ", hostname=server_ip)
    msg = subscribe.simple(player_input, hostname=server_ip)

def distance_calculator ():
    _,img = cam.read()
    output = img.copy()
    measured_radius = 0.625 #in feet
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
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 9999, param2=50, minRadius=1, maxRadius=500)
    # while circles.size() is not 1:

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            ##cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            ##cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # do calculation with diameter (2*r) to figure out distance of circle from camera
            angle_of_target = ((2*r)/horizontal_pixels)*field_of_view #70 degree field of view angle(in radians)
            if angle_of_target > 0:
                distance_to_target = measured_radius/math.tan(angle_of_target) #distance calculator
            else:
                distance_to_target = 1

            h, w, _ = img.shape
            ##print(distance_to_target)
            ##cv2.putText(output, "%d pixels wide circle." % (2*r), (w - 150, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 255], 2)

        # show the output image
        ##cv2.imshow("output", np.hstack([img, output]))
        cv2.waitKey(1)
    return distance_to_target
   

#cam = cv2.VideoCapture(0)


print("\n\n\n\n\n\n            Take your movement and press the button              \n\n\n\n\n\n\n\n") #DISPLAY SOMETHING

time.sleep(5)

button_prompt()
  
print("button pressed, prompting webcam to take a picture") #TAKE A PICTURE WITH WEBCAM
#loc2 = distance_calculator()
#print(loc2)

time.sleep(2)
publish.single(game_update_location, " ", hostname=server_ip)

print("Listening for spell choices")

msg = subscribe.simple(player_input, hostname=server_ip, msg_count=3)
spell_a = str(msg[0].payload)
spell_b = str(msg[1].payload)
spell_c = str(msg[2].payload)


print("I got the possible spells. Going to display them and prompt user to make choice") #DISPLAY SOMETHING
print(spell_a)
print(spell_b)
print(spell_c)

button_prompt()

print("I got the spell selection choice.") #DISPLAY SOMETHING

button_prompt()

print("Prompting gesture and speech recognition")

publish.single(start_recognition, " ", hostname=server_ip)
msg = subscribe.simple(recognition_results, hostname=server_ip, msg_count=2)

msg0 = str(msg[0].payload)
msg1 = str(msg[1].payload)

#guessed_word = '0'
#guessed_gesture = '0'


print(msg0)
print(msg1)

print("goodbye")