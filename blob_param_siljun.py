import cv2
import numpy as np

def setting(stage):### stage=0 -> shingho , stage=1->parking

	if stage==0: #shinho
		# Setup SimpleBlobDetector parameters.
		params = cv2.SimpleBlobDetector_Params()
		 
		# Change thresholds
		params.minThreshold = 0;
		params.maxThreshold = 256;
		 
		# Filter by Area.
		params.filterByArea = True
		params.minArea = 15
		params.maxArea=120
		 
		# Filter by Circularity
		params.filterByCircularity = True
		params.minCircularity = 0.5
		 
		# Filter by Convexity
		params.filterByConvexity = True
		params.minConvexity = 0.1
		 
		# Filter by Inertia
		params.filterByInertia = False
		params.minInertiaRatio = 0.01
		 
		# Create a detector with the parameters
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3 :
		    detector = cv2.SimpleBlobDetector(params)
		else : 
		    detector = cv2.SimpleBlobDetector_create(params)
		return detector


	
	elif stage==1: #parking
		# Setup SimpleBlobDetector parameters.
		params = cv2.SimpleBlobDetector_Params()
		 
		# Change thresholds
		params.minThreshold = 0;
		params.maxThreshold = 256;
		 
		# Filter by Area.
		params.filterByArea = True
		params.minArea = 40
		params.maxArea=300
		 
		# Filter by Circularity
		params.filterByCircularity = True
		params.minCircularity = 0.1
		 
		# Filter by Convexity
		params.filterByConvexity = True
		params.minConvexity = 0.1
		 
		# Filter by Inertia
		params.filterByInertia = True
		params.minInertiaRatio = 0.01
		 
		# Create a detector with the parameters
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3 :
		    detector = cv2.SimpleBlobDetector(params)
		else : 
		    detector = cv2.SimpleBlobDetector_create(params)
		return detector



	

def white_setting(): ### used in jucha stage

	
		# Setup SimpleBlobDetector parameters.
		params = cv2.SimpleBlobDetector_Params()
		 
		# Change thresholds
		params.minThreshold = 0;
		params.maxThreshold = 256;
		 
		# Filter by Area.
		params.filterByArea = True
		params.minArea = 1500
		params.maxArea=400000
		 
		# Filter by Circularity
		params.filterByCircularity = True
		params.minCircularity = 0.1
		 
		# Filter by Convexity
		params.filterByConvexity = True
		params.minConvexity = 0.1
		 
		# Filter by Inertia
		params.filterByInertia = False
		params.minInertiaRatio = 0.01
		 
		# Create a detector with the parameters
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3 :
		    detector = cv2.SimpleBlobDetector(params)
		else : 
		    detector = cv2.SimpleBlobDetector_create(params)
		return detector
