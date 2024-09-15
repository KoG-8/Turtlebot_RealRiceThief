## 2017 R-viz challenge 터틀봇3 오토레이스 부분 우승 & 대통령상 수상

# 레알밥도둑 터틀봇 - 간장게장
![teamlogo](/colorlogo.png)

조원 : [이도규](https://github.com/ldkl123), [정민재](https://github.com/keep9oing), [정현철](https://github.com/junghyeonchiul), [조민수](https://github.com/KoG-8)

연락처 : 정민재, 이도규

## 0. 목차
1. 실행에 앞서

2. 실행법

3. 부분별 세부 설명


## 1. 실행에 앞서
**1.1. 사용한 하드웨어**

![turtlebot](/turtlebot2.jpg)

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

저희가 작성한 소스코드를 전부 실행하려면 라즈베리 카메라 패키지, 웹캠 패키지, 카메라 캘리브레이션, 초음파 센서 설정 등 사전설정이 필요한 것들이 있어 평가측에서 전체를 실행하기에 어려움이 있을것이라 생각합니다. 따라서 센서들이 필요하지 않은 라인트레이싱 부분,주차표지판 검출 부분을 평가 측에서 실행 해 볼 수 있도록 카메라 스크린샷과 간략하게 만든 소스코드를 첨부했습니다. 신호등부분은 저희측에서 대회에서 사용되는 광원을 재현하기에 어려움이있어 첨부하지 못한점 양해부탁드립니다. 혹시 프로그램 실행에 대해 더 궁금하신 점 있으시면 팀원 연락처(정민재 : 010-3833-5688)로 연락 부탁드립니다.


## 3. 부분별 세부 설명

### 3.1. 알고리즘
![graph1](/graph1.png)

![graph2](/Algorithm.png)

### 3.2. 라인트레이싱

turtle_video_siljun.py의 def line_trace에있는 구문입니다.
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

main.py에 있는 def sinho 구문입니다.
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

main.py에 있는 def jucha 구문입니다.
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

main.py에 있는 def chadan 구문입니다.
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



### 3.6. 터널

터널에서는 라이다를 사용하여 터틀봇 주변의 장애물을 파악하여 피하고 방향설정을 통하여 출구로 나가게끔 알고리즘을 구성했다.



**3.6.1. 라이다에서 값을 받아와서 원하는 값으로 가공하는 노드 (in_tunnel1.py)**



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



**3.6.2. 벽을 감지하여 터틀봇에 속도를 보내는 노드 (in_tunnel2.py)**



**3.6.2-1 위치 저장**


만약 이미 지나갔던 곳으로 다시 가게되면 무한루프에 빠질 가능성이 커진다. 따라서 터틀봇의
위치를 알려주는 /odom 토픽 메세지를 받아서 입구를 비롯하여 막혔던 부분의 위치를 저장한다.
~~~
def store_pose():
~~~
위치를 저장하기 직전에 그 위치에 대해서 동작을 실행하면 저장하자마자 실행되므로 일정한 거리를	
빠져나오게 한 뒤에 실행하도록 했다. Past_number이 플래그 역할을 수행한다. 

우선 0 으로 저장한 뒤에 위치를 빠져나오면 1로 바꾸도록 하였다.
~~~
past_number.append(0)
...
if  X > 0.1 and Y > 0.1:
	past_number[i] = 1
~~~

만약 갔었던 위치로 다시가면 방향을 틀도록 했다.
~~~
while check < 10000:		
	print('visited place')
	destination1(Flag)
~~~

**3.6.2-2 장애물이 없을 때 터틀봇의 행동**

장애물이 없다면 터틀봇이 나가아햐는 출구쪽을 바라보고 주행하도록 하였다.
터틀봇이 터널을 인식하여 들어가는 순간 나가야하는 출구는 왼쪽으로 45도
각도에 있기 때문에 /odom 토픽이 제공하는 글로벌 좌표와 틀어진 각도와
글로벌 좌표를 사용하여 로컬 좌표를 만든다.
  터틀봇이 입장하는 순간 새로운 X-Y자표를 만들기 위해서 회전행렬 변환을 써서
앞으로 터틀봇이 이동하는 좌표를 터널 입장시에 형성되는 로컬 좌표의 단위벡터에
의거해서 변환하여 보여준다.
  
입장시에 초기각도와 초기 좌표를 저장한다.
~~~

dot[0] = data.pose.pose.position.x    # 초기 좌표
dot[1] = data.pose.pose.position.y

init_deg = math.degrees(math.pi/2-2*asin(data.pose.pose.orientation.z))  #초기 각도

if init_deg < 0:
	init_deg = 360 + init_deg
	init_ori = math.radians(init_deg)
~~~

초기좌표를 사용하여 회전행렬을 만든다.
~~~
matrix_angle = [[math.cos(init_ori), -math.sin(init_ori)],[math.sin(init_ori), math.cos(init_ori)]]
~~~

글로벌 좌표에서 입장할때의 좌표를 0,0으로 평행이동하고, 터틀봇의 위치도 평행이동한다.
~~~
global_pose[0] = pose[0] - dot[0]
global_pose[1] = pose[1] - dot[1]
~~~

입장후 업데이트되는 글로벌 좌표들에 대하여 회전행렬을 곱하면 로컬 좌표가 완성된다.
~~~
local_pose[0] = matrix_angle[0][0]*global_pose[0] + matrix_angle[0][1]*global_pose[1]
local_pose[1] = matrix_angle[1][0]*global_pose[0] + matrix_angle[1][1]*global_pose[1]
~~~

터들봇의 위치에 따라서 출구방향을 바라봐야하는 각도가 달라진다. 따라서 로컬 좌표와
출구 좌표의 기울어진 각도를 구해서 목표 각도를 만든다.
~~~
angle_goal = math.degrees(atan((2-local_pose[1])/(2+local_pose[0])))
~~~

터틀봇이 바라보는 방향에 따라서 목표 각도의 왼쪽 오른쪽을 판단하여 회전방향을 정한다.
~~~
if ori < 270 + angle_goal and ori > 90 + angle_goal:
~~~
방향을 정해서 그 방향으로 나아가면 출구쪽으로 진행하게 된다.


**3.6.2-3 장애물이 있을 때 터틀봇의 행동**



2-2의 행동보다 장애물이 있을 때의 행동이 우선순위 이므로 장애물을 감지하면 바로 다른
행동을 취한다.

전면부 라이다의 값들을 받아서 10개의 값들중에서 6개이상이 지정한 거리보다 적으면 막다른
벽으로 판단하고 제자리 회전을 수행한다.
~~~
for i in range(0, len(data)):
	if data[i] < 0.2 and data[i] > 0:
		counting = counting+1

rospy.loginfo('strange wall')
...
rospy.loginfo('End')
~~~
정면에 그냥 벽만 있다면 왼쪽 오른쪽 사이드의 거리값을 비교하여 거리가 먼쪽으로 회전하도록 하였다.
~~~
if Lidar[9] > Lidar[10]:
	...
	rospy.loginfo('turn_Left')
else:
	...
	rospy.loginfo('turn_Right')


~~~

만약 터틀봇 사이드에 벽이 있다면 벽을 피하기 위해 벽의 반대방향으로 방향을 설정하여 
이동과 동시에 회전을 한다.
~~~
def scan_wall2(data):
	...
	if temp <= 0.20 and number <= 3:
		...
	elif temp <= 0.23 and number > 3:
		...
	

if bool_way[0] == 1:
	...
 	else:
		while check <= 50:
			destination4(bool_way[1])
			check = check+1
		check = 0
~~~




