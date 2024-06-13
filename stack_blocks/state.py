
class State:
    def __init__(self, num_items = 1, actions = [], reward = 0, *args, **kwargs):
        self.description = args if args else kwargs
        self.num_items = num_items
        # must contain all possible actions
        self.actions = actions
        self.reward = reward

    
