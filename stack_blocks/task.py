class Task:
    def __init__(self):
        self.location = [0,0]
        pass

    def get_current_state(self):
        return str(self.location)

    def take_action(self, act):
        if act == "R":
            self.location[1]+= 1
        pass

    @abstractmethod
    def get_current_reward(self):
        