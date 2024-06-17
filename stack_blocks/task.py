from abc import ABC, abstractmethod
import action
import state

class Task(ABC):

    def __init__(self):
        self.current_state = None 
        self.states = None
        self.initial_state = None
        self.actions = []

    def get_current_state(self):
        return self.current_state
    
    def set_current_state(self, new_state):
        self.current_state = new_state
    
    def get_current_reward(self):
        return self.current_state.get_reward()
    
    def get_states(self):
        return self.states
    
    def get_actions_length(self):
        return len(self.actions)
    
    @abstractmethod
    def take_action(self, act):
        pass

    def reset(self):
        self.current_state = self.initial_state
        return self.current_state
        

class Task_Stack(Task):
    def __init__(self):
        self.actions = action.Action.ALL
        self.states = [state.State(actions = [0, 1], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions = [2, 4], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions =[], reward = 10, location=[[0, 0, 0], [0, 0, 0]]), 
                   state.State(actions = [3, 4], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions = [], reward = 10, location=[[0, 0, 0], [0, 0, 0]])]
        self.terminal_states = [self.states[2], self.states[4]]
        self.initial_state = self.current_state = self.states[0]
        #self.arm = arm

    def take_action(self, states, action_index, arm):
        action = self.actions[action_index]
        #print("Action in task: ", action)
        return action.execute(states, arm)

    def reset(self):
        # self.arm.goto_cartesian_pose()
        # tell the robot to go to the start position
        super().reset()

    
    
        
'''
class Task_Sort(Task):

class Task_Push(Task):

'''