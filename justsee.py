#!/usr/bin/env python


import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import Int8
from std_msgs.msg import Float32


# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError





######################################################################################################
####################<<< MODULE that we made >>>#######################################################



import turtle_video_siljun

pub=rospy.Publisher('/cmd_vel',Twist,queue_size=5)
pub_stage=rospy.Publisher('/stage',Int8,queue_size=5)

######################################################################################################
###############################<<< Trainnig parking sign >>>##########################################



orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

imgTrainColor=cv2.imread('parking.jpg')
imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

kpTrain = orb.detect(imgTrainGray,None)
kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)



###################################################################################
####################<<< Initial Value Definition >>>###############################




time = rospy.Duration(1.6)

lower_red=np.array([170,160,115]) # HSV Ranges used in sinho
upper_red=np.array([180,255,255])
lower_green=np.array([70,75,140])
upper_green=np.array([88,255,255])

lower_blue=np.array([97,100,45]) # HSV Ranges used in jucha
upper_blue=np.array([115,255,240])

dist_chadan=100 # Sonar sensor initial values
dist_tunnel=100

f_g=1 # Constants in sinho
f_r=0
s_g=0

match_len=0 # Constants in jucha
line_count=0
park_count=0
lt=0

angular=0 # initial angular vel

stage=100 # 100 is nomal (0=sinho, 1=jucha, 2=chadan, 3=tunnel)




######################################################################################
#################################<<< Funtions >>>#####################################






def turtlestop(): ### Function that stop the turtlebot3 when node is shut down

	twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)





def turtlemove(linear,angular): ### Function that move the turtlebot

	rospy.on_shutdown(turtlestop)

	twist=Twist()
	twist.linear.x=linear
	twist.angular.z=angular
	#pub.publish(twist)





def state_jucha(num): ### Function that save value used in jucha from 'in_jucha'
	global number
	number=num





def chadan_dist(distance_chadan): ### Function that save Sonar data used in chadan from sonar sensor
	global dist_chadan
	dist_chadan=distance_chadan.data





def tunnel_dist(distance_tunnel): ### Function that save Sonar data used in tunnel from sonar sensor
	global dist_tunnel
	dist_tunnel=distance_tunnel.data
	






def shinho(blob_ROI,stage,angular): ###Function that run when stage=0

	global f_r; global s_g

	if f_g==1 and f_r==0 and s_g==0:		
		keypoints_red=turtle_video_siljun.find_color(blob_ROI,lower_red,upper_red,stage)  
		print('first green signal detected.')

		if keypoints_red:
			f_r=1
		else:
			turtlemove(0.06,angular)
		return 0

	if f_g==1 and f_r==1 and s_g==0:
		keypoints_green=turtle_video_siljun.find_color(blob_ROI,lower_green,upper_green,stage)	
		print('red signal detected. waiting secondary green signal.')
		turtlemove(0,0)

		if keypoints_green:						
			s_g=1
		return 0

	if f_g==1 and f_r==1 and s_g==1:
		print('second green signal detected.') 
		turtlemove(0.06,angular)
		s_g=2
		return 100
		





def jucha(num,angular): ### Function that run when stage=1


	global line_count; global park_count; global lt;
	print(line_count)

	if line_count==0:

		if num[0]==0:
			turtlemove(0.13,angular)
			return 1

		else:
			line_count=1
			return 1

	elif line_count==1:

		if num[0]==1 and lt==0:
			turtlemove(0.06,angular)
			return 1

		elif num[0]==0 and lt==0:

			if num[1]==1:
				turtlemove(0.11,-0.7)
				rospy.sleep(rospy.Duration(2))
				turtlemove(0.1,0)
				rospy.sleep(rospy.Duration(1.7))
				turtlemove(0,0)
				rospy.sleep(time)
				turtlemove(-0.1,0)
				rospy.sleep(rospy.Duration(1.7))
				turtlemove(-0.11,0.7)
				rospy.sleep(rospy.Duration(2))
				turtlemove(0,0)	
				park_count=1
				lt=1
				return 1

			else:
				lt=1
				return 1
			
		else:			
			turtlemove(0.06,angular)

			if num[0]==1:				
				line_count=2
				return 1

			return 1

	elif line_count==2:

		if num[0]==1 and lt==1:
			turtlemove(0.1,angular)
			return 1

		elif num[0]==0 and park_count==0 and lt==1:
			turtlemove(0.11,-0.7)
			rospy.sleep(rospy.Duration(2))
			turtlemove(0.1,0)
			rospy.sleep(rospy.Duration(2))
			turtlemove(0,0)
			rospy.sleep(time)
			turtlemove(-0.1,0)
			rospy.sleep(rospy.Duration(2))
			turtlemove(-0.11,0.7)
			rospy.sleep(rospy.Duration(2))
			turtlemove(0,0)
			lt=2
			return 1

		elif park_count==1 and lt==1:
			lt=2
			return 1
		else:
			turtlemove(0.06,angular)

			if num[0]==1:
				line_count=3
				return 100

			return 1
	






def chadan(dist): ### Function that run when stage=2

	print(dist)
	
	if dist<17:
		turtlemove(0,0)
		return 2

	else:
		rospy.sleep(rospy.Duration(2))
		return 100
	
	





def tunnel(dist): ### Function that run when stage=3

	print(dist)
	
	if dist<15:		
		return 3

	else:
		return 100	
		



	



def angular_Selecting(ros_data): #Function setting angular velocity

	global angular; 
	np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
	
	
	K = np.array([[  220,     0.  ,  320],
              		[    0.  ,   200,   240],
              		[    0.  ,     0.  ,     1.  ]])

	# zero distortion coefficients work well for this image
	D = np.array([0., 0., 0., 0.])

	# use Knew to scale the output
	Knew = K.copy()
	Knew[(0,1), (0,1)] = 0.5 * Knew[(0,1), (0,1)]
	#cv2.imshow('video_fisheye',image_np)
	img_undistorted = cv2.fisheye.undistortImage(image_np, K, D=D, Knew=Knew)
	
	
	

	####<<< Selecting angular velocity >>>####
	image_np,angular=turtle_video_siljun.line_trace(img_undistorted,stage,verbose=False)
	
	if angular>0.28 or angular<-0.28:
		turtlemove(0.13,angular)
		#print('curve')
	else:
			turtlemove(0.17,angular)
	
		#print('line')	
	#print(angular)
	#########################<<< Show processed image >>>##############################
	cv2.imshow('undistorted', img_undistorted)
	
	cv2.waitKey(1)&0xFF








def Stage_Selecting(ros_data):

	#color picking tool : https://alloyui.com/examples/color-picker/hsv/


        ####<<< Direct conversion to CV2 >>>####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

	

	####<<< DEFINE_ROI >>>####
	blob_ROI=image_np
	parking_ROI=image_np
	


	####<<< Make variance global >>>####
	global stage
	global match_len
	
	



	############################<<< Stage Selecting >>>############################	
	if s_g<2 and stage==100:		
		keypoints_green=turtle_video_siljun.find_color(blob_ROI,lower_green,upper_green,0)
		if keypoints_green:
			stage=0
			print('sinho!')


	if line_count<3 and stage==100:
		keypoints_blue=turtle_video_siljun.find_color(parking_ROI,lower_blue,upper_blue,1)
		if keypoints_blue:
			#print("__blue__")
			match_len=turtle_video_siljun.parking_match(keypoints_blue,image_np,orb,bf,desTrain)
			print(match_len)
			if match_len>=13:
				stage=1
				print('jucha!')


	
	if stage==100:
		if dist_chadan<17 and dist_chadan>0 and dist_tunnel>7 :
			stage=2
			print('chadan!')

		elif dist_tunnel<7 and dist_tunnel>0:
			stage=3
			print('tunnel!')

	
				

	
	#########################<<< Select Function depening on stage >>##########################
	if stage==0:

		stage=shinho(blob_ROI,stage,angular)
	elif stage==1 and number:
		stage=jucha(number.data,angular)

	elif stage==2:
		stage=chadan(dist_chadan)

	elif stage==3:
		stage=tunnel(dist_tunnel)
		
	else:
		print("**********normal**************")
		turtlemove(0.06,angular)
		#if angular>0.28 or angular<-0.28:
		#	turtlemove(0.13,angular)
		#	print('curve')
		#else:
		#	turtlemove(0.18,angular)
	
	

	
	
	#########################<<< Show processed image >>>##############################
	cv2.imshow('video_picam',image_np)
	cv2.waitKey(1)&0xFF
	



	#print(stage)

	########################<<< Pub stage to other node >>>############################
	pub_stage.publish(stage)






######################################################################################################

rospy.init_node('video_processor', anonymous=True)
rospy.Subscriber('/camera/image/compressed2',CompressedImage, Stage_Selecting,  queue_size = 1)
rospy.Subscriber('/camera/image/compressed',CompressedImage, angular_Selecting,  queue_size = 1)
rospy.Subscriber('/state',Int8MultiArray,state_jucha)
rospy.Subscriber('/sonar_dist_pub2',Float32,chadan_dist)
rospy.Subscriber('/sonar_dist_pub1',Float32,tunnel_dist)






rospy.spin()
	
######################################################################################################
