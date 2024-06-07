import gridtemplate
import random
import numpy as np
actions = {0:"up", 1:"down", 2:"left", 3:"right"}
word = actions[1]
current_state = [0, 1]
def get_possible_actions(state):
    state = [0, 0]
    possible_actions = [0, 1, 2, 3]
    for i in possible_actions:
        print(i)
    if (state[0] == 0):
        # we can't move up
        possible_actions.remove(0)
    if (state[0] == 2):
        # we can't move down
        possible_actions.remove(1)
    if (state[1] == 0):
        # we can't move left
        possible_actions.remove(2)
    if (state[1] == 2):
        # we can't move right
        possible_actions.remove(3)
    for i in possible_actions:
        print(i)
get_possible_actions(current_state)
# next_action = getattr(grid, word)(current_state)
# print(next_action)


