#Notice: fill out row 67 and download cv2 and numpy

import cv2
import os
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 
from datetime import datetime
from time import sleep
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

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
		cv2.imwrite('//home//pi//Pictures//Recent_Picture.jpg', image)
		
        ########################################
        #######Dropbox upload script start######
        ########################################
        
        # Access token (yes, use '')
        TOKEN = 'token here'

        # These are examples (linux)
        LOCALFILE = '//home/guy//Pictures//Recent_Picture.jpg' # File path use // not /
        BACKUPPATH = f'/{current_time}.jpg' # LEAVE THE / IN - then name you're file


        # Uploads contents of LOCALFILE to Dropbox
        def backup():
            with open(LOCALFILE, 'rb') as f:
                # We use WriteMode=overwrite to make sure that the settings in the file
                # are changed on upload
                print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
                try:
                    dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
                except ApiError as err:
                    # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
                    print(err)


        # Adding few functions to check file details
        def checkFileDetails():
            print("Checking file details")
        
            for entry in dbx.files_list_folder('').entries:
                print("File list is : ")
                print(entry.name)


        # Run this script independently
        if __name__ == '__main__':
            # Check for an access token
            if (len(TOKEN) == 0):
                sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

            # Create an instance of a Dropbox class, which can make requests to the API.
            print("Creating a Dropbox object...")
            dbx = dropbox.Dropbox(TOKEN)

            # Check that the access token is valid
            try:
                dbx.users_get_current_account()
            except AuthError as err:
                sys.exit(
                    "ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

            checkFileDetails()

            print("Creating backup...")
            # Create a backup of the current settings file
            backup()

            print("Done!")

            #deletion
            print("deleting old file...")
            os.remove("Recent_Picture.jpg")
            print("Done!")

        ######################################
        #######Dropbox upload script end######
        ######################################

        sleep(20)


	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == 27:
		break

cv2.destroyAllWindows()
