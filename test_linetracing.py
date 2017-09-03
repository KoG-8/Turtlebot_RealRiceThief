import cv2
import numpy as np
import turtle_video_siljun
stage=100

while(1):
	img=cv2.imread('line_tracing2.png')
	

	image_np,angular=turtle_video_siljun.line_trace(img,stage,verbose=False)



	#########################<<< Show processed image >>>##############################
	cv2.imshow('video',img)
	cv2.waitKey(1)&0xFF

