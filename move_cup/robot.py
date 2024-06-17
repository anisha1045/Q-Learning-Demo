class Robot:
    def __init__(self):
        self.current_state = [0.397, 0.173, 0.015]
        
    def goto_cartesian_pose(self, x, y, z):
        self.current_state = [x, y, z]
        print("Going to: ", self.current_state)
