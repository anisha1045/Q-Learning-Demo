import numpy as np
import armpy
import rospy
#import robot

rospy.init_node("test", anonymous = True)
arm = armpy.kortex_arm.Arm()

class Grid_Template:

    def __init__(self):
        self.grid_dim = 3
        self. grid = [[(0, 0) for _ in range(self.grid_dim)] for _ in range(self.grid_dim)]
        self.distance_delta = 0.05
        self.initial_row = 0.397
        self.initial_col = 0.173
        self.current_coordinates = [self.initial_row, self.initial_col]
        self.terminal_state = [2, 2]
        self.constant_z = 0.015
        
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
               self.grid[i][j] = (-i * self.distance_delta + self.initial_col, j * self.distance_delta + self.initial_col)

    def move_robot(self, row, col):
        current_state = [row, col]
        current_coordinates = self.grid[row][col]
        #robot.goto_cartesian_pose(current_coordinates[0], current_coordinates[1], self.constant_z)
        arm.goto_cartesian_pose(current_coordinates[0], current_coordinates[1], self.constant_z)
        print("robot moving")
        print("Current State: ", current_state)
        return current_state

    def up(self, current_state):
        new_row = current_state[0] - 1
        new_col = current_state[1]
        return self.move_robot(new_row, new_col)

    def down(self, current_state):
        new_row = current_state[0] + 1
        new_col = current_state[1]
        return self.move_robot(new_row, new_col)

    def left(self, current_state):
        new_row = current_state[0]
        new_col = current_state[1] - 1
        return self.move_robot(new_row, new_col)

    def right(self, current_state):
        new_row = current_state[0]
        new_col = current_state[1] + 1
        return self.move_robot(new_row, new_col)

    def reset(self):
        arm.home_arm()
        arm.arm_goto_cartesian(self.initial_row, self.initial_col, self.constant_z)
        #robot.goto_cartesian_pose(self.initial_row, self.initial_col, self.constant_z)
        current_state = [0, 0]
        print("reset done")
        return current_state
