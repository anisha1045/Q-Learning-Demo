
class State:
    def __init__(self, actions = [], reward = 0, *args):
        self.description = args
        # must contain all possible actions
        self.actions = actions
        self.reward = reward

    
