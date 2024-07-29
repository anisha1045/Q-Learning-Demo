import random as rm
import numpy as np
import state

# TO DO CHECK NUM STEPS - 1 IN LEGIB
def func(new_state, num_steps, goal):
    legibility = 0
    denom = 0
    opt_steps = [
        [[2, 4], [3, 3], [4, 2]],
        [[1, 3], [2, 2], [3, 1]],
        [[0, 2], [1, 1], [2, 0]]
    ]
    goals = [(3 - 1, 0), (3 - 1, 3 - 1)]
    if (new_state in goals):
        return 1
    index = 0
    for end_goal in goals:
        print('OPT FROM STARTE: ', opt_steps[0][1][index])
        prob_current_goal = 1 / len(goals)
        print("OPT STEPS: ", opt_steps[new_state[0]][new_state[1]][index])
        numerator = np.exp(-num_steps -opt_steps[new_state[0]][new_state[1]][index]) / np.exp(-opt_steps[0][1][index])
        denom += (numerator * prob_current_goal)
        legibility = numerator * prob_current_goal
        print("LEGIB OF FIRST: ", legibility)
        if (end_goal == goal):
            legibility = prob_current_goal * numerator
        index += 1
    print("LEGIBILITY: ", legibility / denom)

array = [[0.9817687595280431, True], [0.018231240471956785, True]]
num_array = [item[0] for item in array]
print("ARG MAX: ", np.argmax(num_array))

