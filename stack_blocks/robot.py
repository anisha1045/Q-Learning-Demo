#import rospy
#import armpy 

class Robot:

    def __init__(self):

        #rospy.init_node("test", anonymous = True)
        #self.arm = armpy.kortex_arm.Arm()
        #self.arm = armpy.initialize("gen3_lite")
        #self.arm.home_arm()
        self.arm = "Hi I am arm"

    def reset(self, x, y, z):
       self.x1 = x
       self.x2 = y
       self.x3 = z

    def goto_cartesian_pose(self, x,y,z):
        self.arm.goto_cartesian_pose([x,y,z,0,0,1], relative = True) 

    def home_arm(self):
        self.arm.home_arm()
    

    