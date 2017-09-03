import cv2
import numpy as np


######################################################################################################
####################<<< MODULE that we made >>>#######################################################



import blob_param_siljun



######################################################################################################
###############################<<< Functions >>>######################################################






def parking_match(imgCamColor,orb,bf,desTrain): ### Jucha sign recognition 

	imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
	kpCam = orb.detect(imgCamGray,None)
	kpCam, desCam = orb.compute(imgCamGray, kpCam)
	matches = bf.match(desCam,desTrain)
	dist = [m.distance for m in matches]
	dist.sort()		

	wow=[]

	for d in dist:
		if d<38:
			wow.append(d)
		else:
			break

	return len(wow)






def find_color(frame,lower,upper,stage):  ### Color detecting to find sinho_signal or jucha_sign

	detector=blob_param_siljun.setting(stage)

		
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) ### process rgb_image to hsv_image 
	mask_red=cv2.inRange(hsv,lower,upper)


	reversmask=255-mask_red ### Detect blobs
	keypoints = detector.detect(reversmask)

	return keypoints ### return Whether it finds color

	





def find_white(frame,lower,upper): ### detect white blob when jucha_stage

	cv2.line(frame,(int(frame.shape[1]*6.1/9),0),(int(frame.shape[1]*6.1/9),frame.shape[0]),(255,0,255),4) ### draw ROI
	cv2.line(frame,(int(frame.shape[1]*2.9/9),0),(int(frame.shape[1]*2.9/9),frame.shape[0]),(255,0,255),4)
	cv2.line(frame,(int(frame.shape[1]*2.9/9),frame.shape[0]),(int(frame.shape[1]*6.1/9),frame.shape[0]),(255,0,255),4)
	cv2.line(frame,(int(frame.shape[1]*2.9/9),0),(int(frame.shape[1]*6.1/9),0),(255,0,255),4)


	detector=blob_param_siljun.white_setting()
	

	blob_ROI=frame[:,frame.shape[1]*3/9:frame.shape[1]*6/9] ### setting ROI
		

	hsv=cv2.cvtColor(blob_ROI,cv2.COLOR_BGR2HSV) ### process rgb_image to hsv_image 
	mask_red=cv2.inRange(hsv,lower,upper)


	reversmask=255-mask_red ### Detect blobs
	keypoints = detector.detect(reversmask)


	return keypoints






def find_line(frame): ### detect line when jucha_stage	

	blob_ROI=frame[:,frame.shape[1]*3.8/9:frame.shape[1]*5.2/9] ### setting ROI

	gray=cv2.cvtColor(blob_ROI,cv2.COLOR_BGR2GRAY) ### Image process to make detecting line easy	
	ROI=cv2.GaussianBlur(gray,(7,7),0)
	thr=cv2.adaptiveThreshold(ROI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	blur=cv2.medianBlur(thr,9)	
	edge=cv2.Canny(blur,180,360)


	lines=cv2.HoughLines(edge,1,np.pi/180,120) ### detecting lines
	i=0 ### line initializing


	if lines is not None:
		lines=[l[0] for l in lines]
		for line in lines:
			r,th=line
			a=np.cos(th)
			b=np.sin(th)
			x0=a*r
			y0=b*r
			x1=int(x0+1000*(-b))
			y1=int(y0+1000*a)
			x2=int(x0-1000*(-b))
			y2=int(y0-1000*a)
			
			
			cv2.line(frame,(x1+int(frame.shape[1]*3.8/9),y1),(x2+int(frame.shape[1]*3.8/9),y2),(255,0,255),5)
			i+=1 ### line count

	
	return i ### return number of line








def line_trace(frame,stage,verbose): ### find line then return angular velocity
	

	cv2.line(frame,(135,345),(505,345),(253,244,8),2) ### draw ROI
	cv2.line(frame,(135,345),(135,480),(253,244,8),2)
	cv2.line(frame,(505,345),(505,480),(253,244,8),2)


	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) ### Process image to make finding line easy
	ROI=gray[350:,140:500]
	ROI=cv2.GaussianBlur(ROI,(7,7),0)
	thr=cv2.adaptiveThreshold(ROI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	blur=cv2.medianBlur(thr,9)	
	edge=cv2.Canny(blur,180,360)


	if stage==1:### parking
								
		left_edge=edge[:,:edge.shape[1]/2] ### in left side, it finds only '/'type when jucha stage
		right_edge=edge[:,edge.shape[1]/2:] ### in right side, it finds only '\'type when jucha stage
		L_lines=cv2.HoughLinesP(left_edge,1,np.pi/180,10,15,20)
		R_lines=cv2.HoughLinesP(right_edge,1,np.pi/180,10,15,20)


		lineL=[] ### value initializing
		lineR=[]
		L=0	
		R=0
		i=0
		Ldegree=0
		Rdegree=0


		if R_lines is not None:
			R_lines=[l[0] for l in R_lines]
			for line in R_lines:
			
				x1,y1,x2,y2=line ### point that consist of line
				degree=np.arctan2(y2-y1,x2-x1)*180/np.pi
				if degree>0 and R==0:
					i+=1
					Rdegree=degree*1.03
					lineR.append(line)
					R+=2

					cv2.circle(frame,(x1+320,y1+350),10,(0,0,255),-1) ### draw the line that it detect
					cv2.circle(frame,(x2+320,y2+350),10,(255,0,255),-1)
					cv2.line(frame,(x1+320,y1+350),(x2+320,y2+350),(0,100,100),3)
					break
				else:
					continue
			
		if L_lines is not None:
			L_lines=[l[0] for l in L_lines]
			for line in L_lines:
			
				x1,y1,x2,y2=line
				degree=np.arctan2(y2-y1,x2-x1)*180/np.pi
				if degree<0 and L==0:	
					i+=1
					Ldegree=degree*1.03
					lineL.append(line)
					L+=2

					cv2.circle(frame,(x1+140,y1+350),10,(0,0,255),-1) ### draw the line that it detect
					cv2.circle(frame,(x2+140,y2+350),10,(255,0,255),-1)
					cv2.line(frame,(x1+140,y1+350),(x2+140,y2+350),(0,100,100),3)
					break
				else:
					continue

	else: ### in most of stage

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


	
	if verbose is True: ### discribe the existence of line and angle and number
		print('lineL is')
		print(lineL)
		print(Ldegree)
		print('lineR is')
		print(lineR)
		print(Rdegree)
		print('there is %d lines'%(i))	
	

	if i==2:
		return frame,(Ldegree+Rdegree)*0.012 ### if there are two lines, then angular_vel depends on difference of angle


	elif i==1: ### if there are one line, then angular_vel depends on that's inverse number
		if Ldegree==0:
			return frame,(18/(Rdegree+1.9))
		else:
			return frame,(18/(Ldegree-1.9))

	else:
		return frame,0 ### if line not exist, then return 0 angular_vel
