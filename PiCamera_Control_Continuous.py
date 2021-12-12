import cv2
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 
from datetime import datetime
from time import sleep

#datetime section start

#print("current Time =", current_time) #datetime test
#datetime end

#def nothing(x):
#    pass
 
# cv2.namedWindow("Trackbars")
 
# cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 2

rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	#print(gray_image)
	if cv2.countNonZero(gray_image) < 1000:
		print("black")

	else:
		print("not black")
		now = datetime.now()
		current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
		#camera.capture(f'//home//pi//Pictures//{current_time}.jpg')
		sleep(2)
		cv2.imwrite(f'//home//pi//Pictures//{current_time}.jpg', image)
		sleep(20)


	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == 27:
		break

cv2.destroyAllWindows()
