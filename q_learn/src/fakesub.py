#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import pub


class Fake_Sub:
 
 
  def __init__(self):

     self.bridge = CvBridge()
     self.cv_image = None
     self.current_position = ""
     self.pos = None
     self.pub = pub.Color_Detection_Pub()
 
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
     split_list = self.current_position.split(' ')
     self.pos = tuple(map(int, split_list))
     print("Current Pos: ", self.pos)
     return rospy.loginfo(f"Current Position: {self.current_position}")
   
  def color_detection_subscriber(self):
    # TO DO: image_callback and position_callback have those yellow squiggly lines
     try:
        rospy.init_node('color_detection_subsriber', anonymous=True)
        rospy.Subscriber('color_detection/image', Image, self.image_callback)
        rospy.Subscriber('color_detection/position', String, self.position_callback)
        rate = rospy.Rate(1)
        #rate.sleep()
        rospy.spin()
     except rospy.ROSException:
        pass  
     # CHANGE THIS IF NEEDED: 
     return self.pos

  def get_pos(self):
      self.color_detection_subscriber()
      print("Returning: ", self.pos)
      return self.pos

if __name__ == '__main__':
    try: 
         sub = Color_Detect_Sub()
         sub.color_detection_subscriber()
    except rospy.ROSInterruptException:
        pass  