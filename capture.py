import cv2

cam = cv2.videoCapture(0)
img_counter = 0
img_name = "opencv_frame_{}.png".format(img_counter)
cv2.imwrite(img_name, frame)
print("{} written!".format(img_name))

cam.release()

cv2.destroyAllWindows()