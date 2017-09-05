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


###################################################################################
####################<<< Initial Value Definition >>>###############################




time = rospy.Duration(1.6)

dist_tunnel=100


stage=100 # 100 is nomal (0=sinho, 1=jucha, 2=chadan, 3=tunnel)




######################################################################################
#################################<<< Funtions >>>#####################################

def turtlestop():
	
	twist=Twist()
	twist.linear.x=0
	twist.angular.z=0
	pub.publish(twist)

def turtlemove(linear,angular): ### Function that move the turtlebot

	rospy.on_shutdown(turtlestop)

	twist=Twist()
	twist.linear.x=linear
	twist.angular.z=angular
	pub.publish(twist)

def tunnel_dist(distance_tunnel): ### Function that save Sonar data used in tunnel from sonar sensor
	global dist_tunnel
	dist_tunnel=distance_tunnel.data
	


def tunnel(dist): ### Function that run when stage=3

	print(dist)
	
	if dist<15:		
		return 3

	else:
		return 100	
		


def Stage_Selecting(ros_data):
	global stage
	print('distance')
	print(dist_tunnel)
	if stage==100:

		turtlemove(0.04,0)

		if dist_tunnel<15:
			stage=3
			print('tunnel!')

	elif stage==3:
		stage=tunnel(dist_tunnel)	
				

	

	pub_stage.publish(stage)






######################################################################################################


rospy.Subscriber('/camera/image/compressed',CompressedImage, Stage_Selecting,  queue_size = 1)
rospy.Subscriber('/sonar_dist_pub',Float32,tunnel_dist)
pub=rospy.Publisher('/cmd_vel',Twist,queue_size=5)
pub_stage=rospy.Publisher('/stage',Int8,queue_size=5)
rospy.init_node('video_processor', anonymous=True)

rospy.spin()
	
######################################################################################################
