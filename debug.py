import grid
import random
actions = {1:"up", 2:"down", 3:"left", 4:"right"}
word = actions[random.randint(0, 3)]
next_action = getattr(grid, word)()
current_state = [0, 0]

def __main__():
    current_state.
