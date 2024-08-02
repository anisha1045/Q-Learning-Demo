#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class Color_Detect_Sub:
 
 
  def __init__(self):
     self.bridge = CvBridge()
     self.cv_image = None
     self.current_position = ""
 


  def image_callback(self, data):
     try:
        self.cv_image =  self.bridge.imgmsg_to_cv2(data, "bgr8")
        rospy.loginfo("Image received")
        rospy.Rate(1)
     except CvBridgeError as e:
        rospy.logerr(e)
  


  def position_callback(self, data):
     global current_position
     self.current_position = data.data
     return rospy.loginfo(f"Current Position: {self.current_position}")
    




  def display_image(self):
        while not rospy.is_shutdown():
           if self.cv_image is not None:
                 cv2.imshow("Detected Image", self.cv_image)
             
        cv2.destroyAllWindows()
   


  def color_detection_subscriber(self):
    # TO DO: image_callback and position_callback have those yellow squiggly lines
     rospy.init_node('color_detection_subsriber', anonymous=True)
     rospy.Subscriber('color_detection/image', Image, self.image_callback())
     rospy.Subscriber('color_detection/position', String, self.position_callback())
     rate = rospy.Rate(1)
     #rate.sleep()
     self.display_image()
     rospy.spin()
     # CHANGE THIS IF NEEDED: 
     return self.current_position


if __name__ == '__main__':
    try:
        sub_object = Color_Detect_Sub()
        sub_object.color_detection_subscriber()
    except rospy.ROSInterruptException:
        pass      