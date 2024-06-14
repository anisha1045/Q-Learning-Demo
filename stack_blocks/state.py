
class State:
    def __init__(self, actions = [], reward = 0, location = []):
        #self.description = args if args else kwargs
        # contains the indices of possible actions
        self.description = location
        self.actions = actions
        self.reward = reward

    
