import numpy as np
#import armpy
#import rospy

#rospcol.init_node("test", anoncolmous = True)
#arm = armpcol.korterow_arm.Arm()

grid_dim = 3
grid = [[(0, 0) for _ in range(grid_dim)] for _ in range(grid_dim)]
distance_delta = 0.05
initial_row = 0
initial_col = 0
current_coordinates = [initial_row, initial_col]
current_state = [0, 0]
terminal_state = (2, 2)
constant_z = 0.5


for i in range(grid_dim):
    for j in range(grid_dim):
        grid[i][j] = (-i * distance_delta + initial_col, j * distance_delta + initial_col)

def move_robot(row, col):
    current_state = [row, col]
    current_coordinates = grid[row][col]
    #arm.goto_cartesian_pose(current_coordinates[0], current_coordinates[1], constant_z)
    #print("robot moving")
    print(current_state)
    return current_state

def up():
    new_row = current_state[0] - 1
    new_col = current_state[1]
    return move_robot(new_row, new_col)

def down():
    new_row = current_state[0] + 1
    new_col = current_state[1]
    return move_robot(new_row, new_col)

def left():
    new_row = current_state[0]
    new_col = current_state[1] - 1
    return move_robot(new_row, new_col)

def right():
    new_row = current_state[0]
    new_col = current_state[1] + 1
    return move_robot(new_row, new_col)

def reset():
    #arm.home_arm()
    #arm.arm_goto_cartesian(initial_row, initial_col, constant_z)
    current_state = [0, 0]
    #print("reset done")
    return current_state
