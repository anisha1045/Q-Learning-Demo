#!/usr/bin/env python3
import rospy
import time
import cv2
from sensor_msgs.msg import Image
import numpy as np
import threading
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError


class Color_Detection_Pub:

   def get_limits(self, color):  #More accuracy for color detection
       c = np.uint8([[color]])
       hsv2 = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
       hue = hsv2[0][0][0]

       #self.lowerLimit = lowerLimit
       #self.upperLimit = upperLimit

       if hue >= 165:
           lowerLimit = np.array([hue - 10, 100, 50], dtype=np.uint8)
           upperLimit = np.array([180, 255, 255], dtype=np.uint8)
       elif hue <= 15:
           lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
           upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
       else:
           lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
           upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
       return lowerLimit, upperLimit
       #self.get_limits()

   def fixHSVRange(h, s, v):   #calibrates the HSV for color detection
       return (180 * h /360, 255 * s /100, 255 * v / 100)

   def zoom_center(self, img, zoom_factor=5):

     y_size = img.shape[0]
     x_size = img.shape[1]
     
     # define new boundaries
     x1 = int(0.5*x_size*(1-1/zoom_factor))
     x2 = int(x_size-0.5*x_size*(1-1/zoom_factor))
     y1 = int(0.5*y_size*(1-1/zoom_factor))
     y2 = int(y_size-0.5*y_size*(1-1/zoom_factor))  
     # first crop image then scale
     img_cropped = img[y1:y2,x1:x2]
     return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)

   def color_detection_publisher(self):

       #Color_Detection_Pub.get_limits()

       rospy.init_node('color_detection_publisher', anonymous=True)
       image_pub = rospy.Publisher('color_detection/image',Image, queue_size=60)
       grid_pos_pub = rospy.Publisher('color_detection/position', String, queue_size=60)
       rate = rospy.Rate(1)
       bridge = CvBridge()

       yellow = [0, 255, 255] #BGR SCALE
       #red = [0,0, 255]
       #blue = [255, 0, 0]
       #orange = [0,150,240]
       cap = cv2.VideoCapture(0)

       kernel = np.ones((2,2), np.uint8)

       while not rospy.is_shutdown():
           ret, frame = cap.read()
           if not ret:
               rospy.logerr("Failed to capture image")
               pass

           height, width, _ = frame.shape #Camera
           max_width = 600
           max_height = 600

           scale_width = max_width / width
           scale_height = max_height / height
           scale = min(scale_width, scale_height)
           new_width = int(width * scale)
           new_height = int(height * scale)
           frame = cv2.resize(frame, (new_width, new_height), interpolation = cv2.INTER_AREA)

           frame = self.zoom_center(frame)

           x1 = new_height // 3 #Vertical Lines
           x2 = 2 * new_height // 3 #Vertical Lines
           y1 = new_height // 3    #Horizontal Lines
           y2 = 2 * new_height //3 #Horizontal Lines

           hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #changing color scaler from BGR to HSV, more accuracy this way
           h, s, v = cv2.split(hsvImage)
           v = cv2.equalizeHist(v) #allows better detection in poor lighting by equalizing the value
           hsvImage = cv2.merge([h, s, v])

           lowerLimit, upperLimit = self.get_limits(color=yellow)
           #lowerLimit, upperLimit = get_limits(color=blue)
           #lowerLimit, upperLimit = get_limits(color=red)
           #lowerLimit, upperLimit = get_limits(color=orange)

           mask = cv2.inRange(hsvImage, lowerLimit, upperLimit) #to get range of color
           #mask_ = Image.fromarray(mask)   # to get box over detection

           params = cv2.SimpleBlobDetector_Params() #Below is for blob detection
           params.filterByArea = True
           params.minArea = 100
           params.maxArea = 10000
           params.filterByCircularity = False  #delete these and the detection accuracy is worse
           params.minCircularity = 0.1
           params.filterByConvexity = False
           params.minConvexity = 0.1
           params.filterByInertia = False
           params.minInertiaRatio = 0.1

           detector = cv2.SimpleBlobDetector_create(params)
           keypoints = detector.detect(mask)

           img_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
           # cv2.imshow('Blob Detection', img_with_keypoints)

           dilation = cv2.dilate(mask, kernel, iterations = 1)
           closing = cv2.morphologyEx(dilation, cv2.MORPH_GRADIENT, kernel)
           closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
           edge = cv2.Canny(closing, 100, 200) #used for edge detection, testing which is best
           contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
           pos_of_grid = ""
      
           for countour in contours:

               areas = [cv2.contourArea(c) for c in contours]
               max_index = np.argmax(areas)
               cnt=contours[max_index]

               x,y,w,h = cv2.boundingRect(cnt)

               center_x = x + w // 2   #this and line below do the math to verify center of grid
               center_y = y + h // 2

               if center_x < x1:   #detects which grid tile the detected object is in
                   col = 0
               elif center_x < x2:
                   col = 1
               else:
                   col = 2

               if center_y < y1:
                   row = 0
               elif center_y < y2:
                   row = 1
               else:
                  row = 2

               pos_of_grid = f"{row} {col}"  #Acquires where the detected object is in the grid
               cv2.putText(frame, pos_of_grid, (x, y- 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)  #text over detected object

           cv2.line(frame, (x1, 0), (x1, height), (0, 255, 0), 2)
           cv2.line(frame, (x2, 0), (x2, height), (0, 255, 0), 2)
           cv2.line(frame, (0, y1), (width, y1), (0, 255, 0), 2)
           cv2.line(frame, (0, y2), (width, y2), (0, 255, 0), 2)
           cropped_frame = frame[0 : 400, 0 : 400]
           cv2.imshow('Window', cropped_frame) #Contour Detection, only the color
           cv2.imshow('edge', edge)    #Edge Detection, Grabs the surroundings edges of the object
           cv2.imshow('Blob Detection', img_with_keypoints)    #Same as contour, but bases detection off the biggest area of detected object

           if pos_of_grid:
               try:
                self.position = pos_of_grid
                grid_pos_pub.publish(pos_of_grid)
               #time.sleep(5)
                rospy.loginfo(f"Published position: {pos_of_grid}") #Publishes the location of object
                rospy.Rate(1)
              
               except rospy.ROSInterruptException as e:
                   rospy.logerr(f"Failed to publish position: {e}")

           try:
               image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
               #time.sleep(5)
               rospy.loginfo("Published Image")    #publishes that the image is being displayed
               rospy.Rate(1)
           except CvBridgeError as e:
               rospy.logerr(f"Failed to publish image: {e}")
      
           #time.sleep(2)
           if cv2.waitKey(1) & 0xFF == ord('q'):
               pass
      
       rate.sleep()
       cap.release()
       cv2.destroyAllWindows()

   def get_position(self):
        # note: self.position is a tuple
        return self.position

if __name__ == '__main__':
    try:
      pub = Color_Detection_Pub()
      pub.color_detection_publisher()
    except rospy.ROSInterruptException:
      pass      


