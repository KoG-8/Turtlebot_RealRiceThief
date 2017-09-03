import cv2
import numpy as np
import turtle_video_siljun

stage=100
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

imgTrainColor=cv2.imread('parking.jpg')
imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

kpTrain = orb.detect(imgTrainGray,None)
kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)

while(1):
	img=cv2.imread('juchapyojipan.png')
	

	match_len=turtle_video_siljun.parking_match(img,orb,bf,desTrain)
	if match_len>=9:
		stage=1
		print('jucha!')



	#########################<<< Show processed image >>>##############################
	cv2.imshow('video',img)
	cv2.waitKey(1)&0xFF

