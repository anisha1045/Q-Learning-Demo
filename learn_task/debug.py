import random as rm
import numpy as np
import state

bob = state.Statee([1, 2], 1, 4, 4)
print(type(bob))
print(bob.set_reward(1))
print(hasattr(bob, 'get_reward()'))
print(bob.description)

