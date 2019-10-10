import cv2
print('setting up webcam')
camera = cv2.VideoCapture(0)
for i in range(1):
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(i)+'.png', image)
del(camera)

print('I took a picture with the webcam!')
