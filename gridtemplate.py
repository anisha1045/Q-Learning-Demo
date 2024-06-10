import numpy as np
import armpy
import rospy
#import robot



class Grid_Template:

    def __init__(self):

        rospy.init_node("test", anonymous = True)
        self.arm = armpy.kortex_arm.Arm()
        self.arm = armpy.initialize("gen3_lite")

        self.grid_dim = 3
        self. grid = [[(0, 0) for _ in range(self.grid_dim)] for _ in range(self.grid_dim)]
        self.distance_delta = 0.1
        self.terminal_state = [2, 2]
        self.x_start = 0.08
        self.y_start = -0.25
        self.z_start = -0.44
        '''for i in range(self.grid_dim):
            for j in range(self.grid_dim):
               self.grid[i][j] = (-i * self.distance_delta + self.initial_col, j * self.distance_delta + self.initial_col)
'''
    def move_robot(self, row, col):
        current_state = [row, col]
        current_coordinates = self.grid[row][col]
        #robot.goto_cartesian_pose(current_coordinates[0], current_coordinates[1], self.constant_z)
        print("x_start: ", self.x_start)
        print("i am here")
        print("y start: ", self.y_start)
        self.arm.goto_cartesian_pose_old([self.x_start, self.y_start, 0.0, 0.0, 0.0, 0.0, 1], relative = True)
        #print("self.arm.goto_cartesian_pose_old([self.x_start, self.y_start, self.z_start, 0.0, 0.0, 0.0, 1], relative = True)robot moving")
        print("Current State: ", current_state)
        return current_state

    def up(self, current_state):
        new_row = current_state[0] - 1
        new_col = current_state[1]
        self.x_start = 0.0
        self.y_start = -self.distance_delta
        print("UP y: ", self.y_start)
        return self.move_robot(new_row, new_col)

    def down(self, current_state):
        new_row = current_state[0] + 1
        new_col = current_state[1]
        self.x_start = 0.0
        self.y_start = self.distance_delta
        return self.move_robot(new_row, new_col)

    def left(self, current_state):
        new_row = current_state[0]
        new_col = current_state[1] - 1
        self.y_start = 0.0
        self.x_start = self.distance_delta
        return self.move_robot(new_row, new_col)

    def right(self, current_state):
        new_row = current_state[0]
        new_col = current_state[1] + 1
        self.y_start = 0.0
        self.x_start = -self.distance_delta
        return self.move_robot(new_row, new_col)

    def reset(self):
        self.arm.home_arm()
        self.x_start = 0.08
        self.y_start = -0.25
        self.z_start = -0.44
        self.arm.goto_cartesian_pose_old([self.x_start, self.y_start, self.z_start, 0.0, 0.0, 0.0, 1], relative = True)
        current_state = [0, 0]
        print("reset done")
        return current_state
