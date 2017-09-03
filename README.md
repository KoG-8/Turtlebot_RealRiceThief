# Turtlebot_RealRiceThief

# 레알밥도둑 터틀봇 - 간장게장
![teamlogo](/colorlogo.png)

조원 : [이도규](https://github.com/ldkl123), 정민재, [정현철](https://github.com/junghyeonchiul), [조민수](https://github.com/KoG-8)

## 0. 목차
1. 실행에 앞서

2. 실행법

3. 부분별 세부 설명


## 1. 실행에 앞서
**1.1. 사용한 하드웨어**

기본 터틀봇 구성품에 더해서 아래 품목을 추가로 사용했습니다.
 
현재 라즈베리파이 보드를 추가하여 2개를 사용하기 위한 작업 도중이며 아래 코드는 라즈베리파이 1개 기준입니다.

  + Raspberry Pi
  
  + Raspberry Pi Camera
  
  + Raspberry Pi Camera - Fisheye Lens (LS-40180)
  
  + Logitech C920 USB Webcam
  
  + 2x HC-SR04 Ultrasonic Sensor



**1.2. 사용한 소프트웨어**

  + ROS Kinetic

  + Python 2
  
  + OpenCV 3
  
  + Arduino Firmware
  
  + Ubuntu 16.04

**1.3. 사용한 오픈소스**
  
  + [raspicam_node](https://github.com/fpasteau/raspicam_node) by [fpasteau](https://github.com/fpasteau)


## 2. 실행법 
2.1. 이렇게

2.2. 저렇게

2.3. 하면

2.4. 됩니다


## 3. 부분별 세부 설명

### 3.1. 알고리즘
알고리즘설명

### 3.2. 라인트레이싱
~~~
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) ### Process image to make finding line easy
	ROI=gray[350:,140:500]
	ROI=cv2.GaussianBlur(ROI,(7,7),0)
	thr=cv2.adaptiveThreshold(ROI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	blur=cv2.medianBlur(thr,9)	
	edge=cv2.Canny(blur,180,360)
~~~
frame이 원본 이미지 입니다.
원본이미지를뒤 각종blur를 사용하여 침식_팽창 과정을 거친 뒤

~~~
lines=cv2.HoughLinesP(edge,1,np.pi/180,30,25,30)


		lineL=[]
		lineR=[]
		L=0	
		R=0
		i=0
		Ldegree=0
		Rdegree=0

		if lines is not None:
			lines=[l[0] for l in lines]
			for line in lines:
				
				x1,y1,x2,y2=line
				degree=np.arctan2(y2-y1,x2-x1)*180/np.pi
				if degree>0 and R==0:
					i+=1
					Rdegree=degree
					lineR.append(line)
					R+=2
					cv2.circle(frame,(x1+140,y1+350),10,(0,0,255),-1)
					cv2.circle(frame,(x2+140,y2+350),10,(255,0,255),-1)
					cv2.line(frame,(x1+140,y1+350),(x2+140,y2+350),(0,100,100),3)
				elif degree<0 and L==0:
					i+=1
					Ldegree=degree
					lineL.append(line)
					L+=2
					cv2.circle(frame,(x1+140,y1+350),10,(0,0,255),-1)
					cv2.circle(frame,(x2+140,y2+350),10,(255,0,255),-1)
					cv2.line(frame,(x1+140,y1+350),(x2+140,y2+350),(0,100,100),3)
				else:
					continue
~~~
houghlinesP를뒤 이용하여 라인을 추출한 뒤

~~~
if i==2:
		return frame,(Ldegree+Rdegree)*0.012 ### if there are two lines, then angular_vel depends on difference of angle


	elif i==1: ### if there are one line, then angular_vel depends on that's inverse number
		if Ldegree==0:
			return frame,(18/(Rdegree+1.9))
		else:
			return frame,(18/(Ldegree-1.9))

	else:
		return frame,0 ### if line not exist, then return 0 angular_vel
~~~
추출한 라인의 각도를 이용하여 line tracing했습니다.

### 3.3. 신호등
~~~
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
~~~

카메라가green_blob을찾으면실행되는함수입니다.
first_green 을나타내는 f_g

first_red 를나타내는 f_r

second_green 을나타내는 s_g

세 전역변수를 이용하여 신호구간을 만들었습니다.

일단 첫번째 초록이 감지되면 실행하는 부분입니다.
빨강이 감지될때까지 라인트레이싱을 하는부분입니다.
return 0 은 stage값을 리턴하는것인데 신호구간의 스테이지값을 0으로 지정해서 그렇습니다.

~~~
if f_g==1 and f_r==1 and s_g==0:
		keypoints_green=turtle_video_siljun.find_color(blob_ROI,lower_green,upper_green,stage)	
		print('red signal detected. waiting secondary green signal.')
		turtlemove(0,0)

		if keypoints_green:						
			s_g=1
		return 0
~~~
첫번째 초록을 감지후 첫번째 빨강을 감지한다면 다음 초록을 감지할때까지 멈춰있는 부분입니다.

~~~
if f_g==1 and f_r==1 and s_g==1:
		print('second green signal detected.') 
		turtlemove(0.06,angular)
		s_g=2
		return 100		
~~~
두번째 초록을 감지하면 일상상태인 stage값 100으로 리턴하여 신호구간을 마칩니다.


### 3.4. 주차
~~~
def jucha(num,angular): ### Function that run when stage=1


	global line_count; global park_count; global lt;
	print(line_count)

	if line_count==0:

		if num[0]==0:
			turtlemove(0.06,angular)
			return 1

		else:
			line_count=1
			return 1
~~~
카메라가 주차표지판을 인식한 뒤 실행하는 함수입니다.
num은 in_jucha.py에서 발행하는 것인데 터틀봇우측에달린 웹캠이 흰선이 검출됬나,주차할 공간이 있는가를 담고있습니다.
line_count는 우측에 선이 몇 번 검출됬나 이고
park_count는 주차를 안한상태면 0 했으면 1입니다.
lt는 알고리즘구현을 위하여 임의로 만든 상수입니다.

num은 [흰선이검출됬나,주차할공간이있는가]로 구성되있습니다.
일단 표지판인식후 우측에선이 검출될때까지 라인트레이싱하는 부분입니다.

~~~
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
~~~
우측에 선이 첫번째로 검출됬을때 주차할 공간이 있으면 주차, 없으면 다음라인을 검출할때까지 라인트레이싱 합니다.

~~~
elif line_count==2:

		if num[0]==1 and lt==1:
			turtlemove(0.06,angular)
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
~~~
두번째로 선을 검출했을때 주차를 이미 한 상태라면 다음선을 검출할때까지 라인트레이싱,주차를 안 한 상태라면 주차를 합니다.
그런뒤 세번째라인을 지나면 일상상태 stage=100으로 돌아가며 주차구간을 종료합니다.


### 3.5. 차단바
~~~
def chadan(dist): ### Function that run when stage=2

	print(dist)
	
	if dist<15:
		turtlemove(0,0)
		return 2

	else:
		rospy.sleep(rospy.Duration(2))
		return 100
~~~
차단바를 감지하기위한 센서가 일정거리 이하를 감지하면 실행되는 터널구간함수입니다.
일정거리 이하를 계속 검출하면 정지, 일정거리 이상이 감지되면 종료됩니다.


설명

### 3.6. 터널

터널에서는 라이다를 사용하여 터틀봇 주변의 장애물을 파악하여 피하고 방향설정을 통하여 출구로 나가게끔 알고리즘을 구성했다.

1. 라이다에서 값을 받아와서 원하는 값으로 가공하는 노드

주로 필요한 정면의 거리값을 배열로 받아서 정면, 왼쪽, 오른쪽으로 나누어서 라벨링한다.

하지만 가끔 라이다 값이 0으로 튀는 일이 발생한다.
~~~
Front_Left_avg = avg(Front_Left)
...
~~~
아래 코드는 튀는 값 0을 제외하고 평균값을 내는 함수이다.
~~~
def avg(data):
	return 	sum(data)/(len(data)-data.count(0)+0.01) 
~~~
평균낸 값을 다른 노드로 보내기 위해서 퍼블리쉬를 한다.
~~~
raw.data = [...]
raw.sharp = [...]
raw.front = [... ]
~~~
data는 전반적인 각도들의 묶음, sharp는 소수개수의 각도의 묶음이다.

다음으로 data2는 왼쪽, 가운데, 오른쪽 중에서 가장 먼곳을 가려내기 위해서 구성된다.
~~~
data2 = [Front_Left_avg, Front_avg , Front_Right_avg]
~~~
Sort로 내림차순으로 배열을 정리하여 가장 큰값을 맨앞으로 보낸다.
~~~
data2.sort(reverse=True)
~~~

그 다음 기존의 data2 배열에서 몇번째 값이였는지 가려내기 위해 find_same 함수를 쓴다.
~~~
find_same(data2[0])
~~~	
값을 찾아내면 그 값의 배열번호를 다른노드로 퍼블리쉬한다.


#!/usr/bin/env python
import rospy
import numpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from wall.msg import raw_sensor_8_10
import sys, select, termios, tty
import copy
from math import atan
from math import asin
import math

global Flag
global check

global flag
global flag2
global count

global num

global dot
global past
global pose
global copy_pose
global past_number

global bool_way



bool_way = [0,0]

num=0
count = 0
dot = [0, 0]
past = [[0,0]]
pose = [0, 0]
copy_pose = [0,0]
past_number = [0]
flag =0
flag2 =0
Flag = 0
check = 0




##############################################################################
####  Publish the process values to '/cmd_vel' node  #########################
##############################################################################

pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 5)
rospy.init_node('vel', anonymous=True)
rate = rospy.Rate(10)
twist = Twist()

##############################################################################



##############################################################################
####  Exit node  #############################################################
##############################################################################

def myhook():               # If Ctrl + c occured, the node ends by myhook function and turtlebot's velocity returns to 0.
	twist = Twist()
	twist.linear.x=0
	twist.angular.z=0
	pub.publish(twist)

##############################################################################

##############################################################################
####  main   #################################################################
##############################################################################

def callback1(data):
	global Flag
	global flag2
	global past
	global count
	global pose
	global copy_pose
	global past_number
	global check
	global bool_way	

	rospy.on_shutdown(myhook)
	Lidar = data.data
	Lidar2 = data.sharp
	Lidar3 = data.front			# Get the processed values from sensor node
	Far = data.Far
	Flag = data.Flag
	
	wall = 0.16				# minimum value of distance from wall turtlebot have to aviod 
	scan_wall2(Lidar2)
	remind_past()				# Consider present position is visited place or not
	
	
	if count == 1:
		while check < 10000:		# If It placed on visited place, turn way back 
			print('visited place')
			destination1(Flag)
			check = check+1
		check=0
		count = 0


	
	
	if scan_wall(Lidar3) == 1:		# If there is wall in front of turtlebot or block way, turn back
		rospy.loginfo('strange wall')
		while check <= 100:
			destination5(3)	
			check = check+1
		check=0	
		rospy.loginfo('End')
	else:	
		if bool_way[0] == 1:		# If there is wall beside the turtlebot
			if Lidar[8] <= wall+0.03 and Lidar[8] > 0: 	# If turtlebot is in uncertain position with blocked wall
				store_pose()
				remind_past()
			
			
				if Lidar[9] > Lidar[10]:		# Compare the left and right side of distance and turn to long distance
					while check<= 100:
						destination5(1)
						rospy.loginfo('turn_Left')
						check = check+1
					check = 0
				else:
					while check <= 100:
						destination5(3)
						rospy.loginfo('turn_Right')
						check = check+1
					check = 0
				
			else:
				while check <= 50:
					destination4(bool_way[1])
					check = check+1
					
				check = 0
				bool_way[0] = 0		# Refresh the values
				bool_way[1] = 0
				
				
				
		else:	
			# If there is no blocks around turtlebot, It goes to exit way using callback4 function
			flag2=0				# Refresh the flag number to store the coordinate again
			callback4()			
			rospy.loginfo('check')

	
	rospy.loginfo('######################################################################')


####  main ends   ############################################################



##############################################################################
####  Functions  #############################################################
##############################################################################

def scan_wall(data):
	counting = 0
	for i in range(0, len(data)):
		if data[i] < 0.2 and data[i] > 0:       # Find the distances which are less 0.2m and counts the number of data 
			counting = counting+1

	
	
	if counting >= 6:				# If the count number of values over 6, turtlebot consider that there is wall
		return 1				# in front of It and returns 1			
	else:
		return 0
	

def scan_wall2(data):
	global bool_way                           
	temp = 0
	number = 0

	for i in range(0, len(data)):			# Accept the front Lidar values and excepting zero value and select the init value 
		if data[i] != 0:
			temp = data[i]
			break	
	
	for j in range(i, len(data)):
		if data[j] < temp and data[j] !=0:	# Compare the values and get the smallest value 
			temp = data[j]
			number = j	
	#rospy.loginfo([temp, number])
	if temp <= 0.20 and number <= 3:
		bool_way[0] = 1				# the smallest value means the wall's postion 
		bool_way[1] = 3				# Return the direction the turtlebot have to go to avoid the wall
		#rospy.loginfo('Right')		
	elif temp <= 0.23 and number > 3:
		bool_way[0] = 1
		bool_way[1] = 1
		#rospy.loginfo('Left')
	

def store_pose():
	global past
	global flag2
	global pose
	global count	
	global copy_pose
	global past_number
	global num 	
	
	if count == 0:
		if flag2==0:
			copy_pose = copy.copy(pose)	# Store the place coordinate which turtlebot must avoid 
			past.append(copy_pose)		# ex) entrance of tunnel
			past_number.append(0)
			num = num+1
			flag2 = 1

		

def remind_past():
	global past
	global pose
	global count
	global past_number


	for i in range(0, len(past)):
			X = abs(pose[0]-past[i][0])	# Subtract the Stored coordinate and the present coordinate 
			Y = abs(pose[1]-past[i][1])
			
			if  X > 0.1 and Y > 0.1:
				#rospy.loginfo('saved')		# After the coordinate stored, turtlebot have to get out the stored position 
				past_number[i] = 1		# so coordinate subtractin over 0.1m makes the past_number 1 	
	
			if  X < 0.1 and Y < 0.1:
				#rospy.loginfo('First step')	# When turtlebot come back to past coordinate make count 1 
				if past_number[i] == 1:		# Count 1 make the turtlebot turns for optional time
					rospy.loginfo([X, Y])
					past_number[i] = 0
					count = 1
			
				
##############################################################################
####  Turtlebot's linear, angular velocity funcation #########################
##############################################################################


def destination1(data1):
	if data1==1:	
		twist.linear.x = 0.0
		twist.angular.z = 0.6
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = 0.0
		twist.angular.z = -0.6            #Right (-) Left (+) 
		pub.publish(twist)


def destination4(data1):
	if data1==1:	
		twist.linear.x = 0.04
		twist.angular.z = 0.5
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = 0.04
		twist.angular.z = -0.5            #Right (-) Left (+) 
		pub.publish(twist)
	
def destination5(data1):
	if data1==1:	
		twist.linear.x = -0.01
		twist.angular.z = 0.6
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = -0.01
		twist.angular.z = -0.6            #Right (-) Left (+) 
		pub.publish(twist)
				
##############################################################################


##############################################################################
#### Converting Global coordinate to Local coordinate  #######################
##############################################################################

def callback3(data):
	global dot
	global flag
	global pose
	global past
	global copy_pose
	global init_ori
	global init_deg
	global angle_goal
	global angle_twisted
	global ori
	global local_pose
	global global_pose
	
	local_pose = [0,0]
	global_pose = [0,0]
	
	if flag ==0:
		dot[0] = data.pose.pose.position.x    		# Using flag to save the initial coordinate which turtlebot starts just one time
		dot[1] = data.pose.pose.position.y
		past[0] = dot	
		copy_pose = copy.copy(dot)			# Copy_pose save the coordinate in past_postition to avoid to heading to 									  entrance
		flag = 1
	
	
	pose[0] = data.pose.pose.position.x			# Updating the coordinate 
	pose[1] = data.pose.pose.position.y 
	
	if flag==1:
		init_deg = math.degrees(math.pi/2-2*asin(data.pose.pose.orientation.z))  # Use flag to save the initial degree from global axis
		if init_deg < 0:
			init_deg = 360 + init_deg		# Convert the degree to 0 ~ 360
		init_ori = math.radians(init_deg)
		flag=2
	
	global_pose[0] = pose[0] - dot[0]			# Parallel translate make initial coordinate to [0,0]
	global_pose[1] = pose[1] - dot[1]	
	 
	
	
	
	ori = math.degrees(math.pi/2-2*asin(data.pose.pose.orientation.z))
	
	if ori < 0:
		ori = 360 + ori					# Present degree while turtlebot is moving and Convert the degree to 0 ~ 360 
	
	ori = ori - init_deg
	
	if ori < 0:
		ori = 360 + ori

	# Using initial degree from global axis to make the rotation matrix 

	matrix_angle = [[math.cos(init_ori), -math.sin(init_ori)],[math.sin(init_ori), math.cos(init_ori)]]	
		
	# Multiply the rotation matrix to present global coordinate and make local coordinate

	local_pose[0] = matrix_angle[0][0]*global_pose[0] + matrix_angle[0][1]*global_pose[1]
	local_pose[1] = matrix_angle[1][0]*global_pose[0] + matrix_angle[1][1]*global_pose[1]
	
	# Calculate the degree turtlebot have to turn and head depend on exit's direction

	angle_goal = math.degrees(atan((2-local_pose[1])/(2+local_pose[0])))

##############################################################################




##############################################################################
#### Making turtlebot turn for heading to exit coordinate  ###################
##############################################################################


def callback4():
	rospy.on_shutdown(myhook)
	
	speed = 0.09
		
	
	if ori < 270 + angle_goal and ori > 90 + angle_goal:	# Catch the turtlebot's present heading and judge which why to turn
		if abs(ori - 270 - angle_goal) < 6:		# If Present degree and desire degree's substraction is lower than 6
			twist.linear.x = speed
			twist.angular.z = -0.0
			pub.publish(twist)
		else:
			twist.linear.x = speed
			twist.angular.z = -0.3
			pub.publish(twist)
	else:
		if abs(ori - 270 - angle_goal) < 6:	
			twist.linear.x = speed
			twist.angular.z = -0.0
			pub.publish(twist)
		else:
			twist.linear.x = speed
			twist.angular.z = 0.3
			pub.publish(twist)


def listen():
	rospy.Subscriber('/odom', Odometry, callback3)
	rospy.Subscriber('/raw_sensor', raw_sensor_8_10, callback1)
	rospy.spin()


if __name__ == '__main__':
	listen()
~~~



설명



