#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import Int8

# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError


######################################################################################################
####################<<< MODULE that we made >>>#######################################################


import turtle_video_siljun



###################################################################################
####################<<< Initial Value Definition >>>###############################


white_detected=0
park_enable=0

lower_white=np.array([0,0,200]) ### HSV range used in white detect
upper_white=np.array([180,15,255])

stage=100


######################################################################################
#################################<<< Funtions >>>#####################################



def checking_stage(ss): ### Function that save the stage value from 'main'
	global stage
	stage=ss.data
	




def checking_distance(lidar): ### Funtion that save the distance from lidar
	global d
	d=lidar.ranges[250:330]





def parking_possiblity(ros_data): ### using web_cam, check white_blob and line and enough distance, if all exist, it send Availablity
	
    global white_detected; global park_enable; global d
    
    if stage is 1:	
    	
   	np_arr = np.fromstring(ros_data.data, np.uint8) ### image process
    	frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    	mask_white=cv2.inRange(hsv,lower_white,upper_white)
   	res1=cv2.bitwise_and(frame,frame,mask=mask_white)
    	

    	line=turtle_video_siljun.find_line(frame) ### Checking if there are lines
	keypoints=turtle_video_siljun.find_white(frame,lower_white,upper_white) ### Checking if there are white
	
	
	

	if line>0 and keypoints:				
		white_detected=1   ### check white line
	else:
		white_detected=0
		

	
	n=1
	for i in d:
		if i>0.12 and i<0.6:
			n=0		### check parking space
	if n ==0:
		park_enable=0
	else:
		park_enable=1	
		
		

    	
    	
    	cv2.imshow('frac',frame) ### show processd image
	cv2.imshow('white',res1)
    	cv2.waitKey(1)&0xFF
    	
	
	print(white_detected)
	
    
    state=Int8MultiArray()
    state.data=[white_detected,park_enable]
    pub1.publish(state) ### pub white_detected and park_enable to 'main'
    

###########################################################################################################

rospy.Subscriber('/scan',LaserScan,checking_distance)
rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage, parking_possiblity,  queue_size = 1)
rospy.Subscriber('/stage',Int8,checking_stage)

pub1=rospy.Publisher('state',Int8MultiArray,queue_size=5)


rospy.init_node('video_processor2', anonymous=True)
rospy.spin()

