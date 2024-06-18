
class State:
    def __init__(self, actions = [], reward = 0, *args, **kwargs):
        self.desc = args if args else kwargs
        # contains the indices of possible actions
        #self.description = location
        self.action_indices = actions
        self.reward = reward

    def get_reward(self):
        return self.reward
    
    def get_action_indices(self):
        return self.action_indices
    
    def to_string(self):
        return str(self.desc) 
