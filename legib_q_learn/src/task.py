from abc import ABC, abstractmethod
import action
import state
import random
import grid
import test

class Task(ABC):

    def __init__(self):
        self.current_state = None 
        self.states = None
        self.initial_state = None
        self.actions = []
        self.terminal_states = []

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
    
    def check_new_terminal(self, terminal):
        if (terminal in self.terminal_states):
            return False
        self.terminal_states.append(terminal)
        return True
    
    @abstractmethod
    def take_action(self, **kwargs):
        pass

    def get_terminal_states(self):
        return self.terminal_states

    def ep_reset(self):
        self.current_state = self.initial_state
        return self.current_state
        
class Task_Many_Goals(Task):
    def __init__(self, grid_dim, start_state, end_states, num_eps, num_learns, test_mode = False):
        self.actions = action.TaskMoveActions.ALL
        print("Task Actions List: ", self.actions)
        self.grid_dim = grid_dim # can change for any grid dimension
        self.states = {}
        for i in range(grid_dim):
            for j in range(grid_dim):
                possible_actions = [0, 1, 2, 3]
                if (i == 0):
                    # we can't move up
                    possible_actions.remove(0)
                if (i == grid_dim - 1):
                    # we can't move down
                    possible_actions.remove(1)
                if (j == 0):
                    # we can't move left
                    possible_actions.remove(2)
                if (j == grid_dim - 1):
                    # we can't move right
                    possible_actions.remove(3)
                self.states[(i, j)] = state.State(possible_actions, -1, i, j)
        # start_state and end_states must be tuples
        self.initial_coordinates = start_state
        self.initial_state = self.current_state = self.states[self.initial_coordinates]
        self.test_mode = test_mode
        if (not test_mode):
            pass
            #self.grid = grid.Grid(grid_dim, self.initial_coordinates)
        self.goal_reward = 10
        self.goals = end_states
        for goal in self.goals:
            self.states[goal].set_reward(self.goal_reward)
            if (not test_mode):
                pass
                #self.test = test.Test(self.states, self.initial_coordinates, self.goals, grid_dim, self.actions, num_eps, num_learns)
                #self.grid.plot_reward(goal)
        self.distance_delta = 0.1
        self.terminal_states = []
        self.last_episode = False
        self.x_start = 0.06
        self.y_start = -0.27
        self.z_start = -0.44
        #self.arm = arm

    @property
    def get_goal_reward(self):
        return self.goal_reward
    
    
    # tells us whether we are in a terminal state and if we are,
    # whether we know about this goal or not
    def check_terminal(self, new_state):
        stop = False
        new = False
        if new_state.get_reward() == self.goal_reward:
            stop = True
            # we check if the new state is a new terminal state or if we've seen it before
            new = super().check_new_terminal(new_state)
        return stop, new

    def get_initial_tuple(self):
        return self.initial_coordinates
    
    def get_initial_state(self):
        return self.initial_state
    
    def change_last_episode(self):
        self.last_episode = True
    
    def get_test_mode(self):
        return self.test_mode

    def choose_terminal(self):
        if (len(self.terminal_states) >= 1):
            return random.choice(self.terminal_states)
        else:
            print("Terminal states is empty. We have not learned them yet.")
        
    def add_terminal(self, new_state):
        self.terminal_states.append(new_state)

    def take_action(self, action_index, arm):
        action = self.actions[action_index]
        #print("Action in task: ", action)
        result_state = action.execute(self.states, self.current_state, self.distance_delta, arm)
        print("result state: ", result_state)
        if (self.last_episode and not self.test_mode):
            pass
            #self.grid.plot_traj(result_state)
            #self.grid.show_plot()
        return self.states[result_state], result_state
    
    def show_plot(self):
        if (not self.test_mode):
            pass
            #self.grid.end()

    def ep_reset(self):
        #self.arm.home_arm()
        self.x_start = -0.22
        self.y_start = -0.23
        self.z_start = -.45
        #arm.goto_cartesian_pose(self.x_start, self.y_start, self.z_start)
        #arm.close_gripper()
        super().ep_reset()

    # at the beginning of every learning phase, reset the number of terminal states known and the list of terminal states
    def learn_reset(self):
        #self.test.reset()
        self.terminal_states = []

    def reset_arm(self, arm):
        arm.open_gripper()
        arm.home_arm()
        x_start = -0.22
        y_start = -0.23
        z_start = -.45
        arm.goto_cartesian_pose(x_start, y_start, z_start)
        arm.close_gripper()

class Task_Stack(Task):
    def __init__(self):
        # CHANGE THIS TO THE SPECIFIC ACTION
        self.actions = action.TaskStackActions.ALL
        self.states = {((0, 0, 0), (0, 0, 0)) : state.State(actions = [0, 1], reward = -1, location=((0, 0, 0), (0, 0, 0))),
                   ((1, 0, 0), (0, 0, 0)) : state.State(actions = [2, 4], reward = -1, location=((0, 0, 0), (0, 0, 0))),
                   ((2, 0, 0), (0, 0, 0)) : state.State(actions =[], reward = 10, location=((0, 0, 0), (0, 0, 0))), 
                   ((3, 0, 0), (0, 0, 0)) : state.State(actions = [3, 4], reward = -1, location=((0, 0, 0), (0, 0, 0))),
                   ((4, 0, 0), (0, 0, 0)) : state.State(actions = [], reward = 10, location=((0, 0, 0), (0, 0, 0)))}
        self.terminal_states = self.states[((2, 0, 0), (0, 0, 0))], self.states[((4, 0, 0), (0, 0, 0))]
        self.initial_state = self.current_state = self.states[((0, 0, 0), (0, 0, 0))]


    def take_action(self, states, action_index, arm):
        action = self.actions[action_index]
        return action.execute(states, arm)

    def ep_reset(self, arm):
        super().ep_reset(arm)
        

    
class Task_Move(Task):
    def __init__(self, grid_dim):
        self.actions = action.TaskMoveActions.ALL
        print("Task Actions List: ",self.actions)
        self.grid_dim = grid_dim # can change for any grid dimension
        self.states = {}
        for i in range(grid_dim):
            for j in range(grid_dim):
                possible_actions = [0, 1, 2, 3]
                if (i == 0):
                    # we can't move up
                    possible_actions.remove(0)
                if (i == grid_dim - 1):
                    # we can't move down
                    possible_actions.remove(1)
                if (j == 0):
                    # we can't move left
                    possible_actions.remove(2)
                if (j == grid_dim - 1):
                    # we can't move right
                    possible_actions.remove(3)
                self.states[(i, j)] = state.State(possible_actions, -1, i, j)
        self.states[(grid_dim - 1, grid_dim - 1)].reward = 10
        self.distance_delta = 0.1
        self.terminal_states = [self.states[(grid_dim - 1, grid_dim - 1)]]
        self.x_start = 0.06
        self.y_start = -0.27
        self.z_start = -0.44
        self.initial_state = self.current_state = self.states[(0,0)]
        #self.arm = arm

    def take_action(self, states, action_index, arm):
        action = self.actions[action_index]
        #print("Action in task: ", action)
        return self.states[action.execute(states, self.current_state, self.distance_delta, arm)]

    def ep_reset(self, arm):
        #self.arm.home_arm()
        self.x_start = 0.06
        self.y_start = -0.27
        self.z_start = -0.44
        arm.goto_cartesian_pose(self.x_start, self.y_start, self.z_start)
        arm.close_gripper()
        super().ep_reset(arm)
        
'''
class Task_Sort(Task):

'''