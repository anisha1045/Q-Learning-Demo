
class State:
    def __init__(self, actions = [], reward = 0, *args, **kwargs):
        self.description = args if args else kwargs
        # must contain all possible actions
        self.actions = actions
        self.reward = reward

    
