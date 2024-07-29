import numpy as np

# we should only be using policy shape object if we've been to a terminal state before
class PolicyShape():
    def __init__(self, states, actions_length, start, grid_dim):
        # dict that mirrors q table, but the values are the resulting states, all values are default to None
        self.feedback_table = {}
        # dict that maps the state objects to their x y tuples
        self.states = {}
        for key in states.keys():
            self.feedback_table[states[key]] = np.full(actions_length, None)
            self.states[states[key]] = key
        self.actions_length = actions_length
        # dictionary mapping terminal states to their indices in the list 
        self.terminal_states = {}
        # dictionary mapping all states to their minimum number of steps from start to end for each terminal state in a list
        self.optimal_steps = np.empty((grid_dim, grid_dim, 0))
        self.start = start
        self.index = 0
        self.default_legibility = 1
        if (len(self.terminal_states)) >= 2:
            self.default_legibility = 1 / len(self.terminal_states)

    def get_weight(self, terminal_state, step_num):
        return self.get_opt_from_start(terminal_state) - step_num

    def get_opt_steps(self, current_state, terminal_state):
        return self.optimal_steps[self.states[current_state][0]][self.states[current_state][1]][self.terminal_states[terminal_state]]
    
    def get_opt_from_start(self, terminal_state):
        return self.optimal_steps[self.states[self.start][0]][self.states[self.start][1]][self.terminal_states[terminal_state]]
    
    def set_opt_steps(self, current_state, terminal_state, updated_num):
        self.optimal_steps[self.states[current_state][0]][self.states[current_state][1]][self.terminal_states[terminal_state]] = updated_num

    def get_feedback(self, current_state, action_index):
        return self.feedback_table[current_state][action_index]

    def update_feedback(self, state, action_index, new_state):
        self.feedback_table[state][action_index] = new_state

    def propagate_opt_steps(self, new_state, terminal_state, stop, states_queue, old_opt_steps, traj_steps, index_best):
        new_opt_steps = self.get_opt_steps(new_state, terminal_state)
        # if new_opt_steps is known and (we don't know some the opt for earlier states or the new_opt is faster) or if we've reached the end
        if (((new_opt_steps != 0) and (old_opt_steps == -1 or old_opt_steps + traj_steps > new_opt_steps)) or stop):
            # go through the queue and update the values accordingly
            # this is the best optimal steps, and we are going to propagate info backwards
            traj_steps = 0
            traj_length = len(states_queue)
            for k in range(len(states_queue)):
                state = states_queue[k]
                opt_steps = self.get_opt_steps(state, terminal_state)
                if (opt_steps == 0 or traj_length - k + new_opt_steps < opt_steps):
                    self.set_opt_steps(state, terminal_state, traj_length - k + new_opt_steps)
            old_opt_steps = new_opt_steps
            index_best = len(states_queue) - 1
        # if we're at a state the opt steps is unknown and we have been to a known opt steps before, propagate info forwards 
        # maybe not making full use of the information if new_opt_steps is known but bigger than it should be but oh well
        elif ((new_opt_steps == 0 or new_opt_steps > old_opt_steps + len(states_queue) - index_best) and not stop and old_opt_steps != -1):
            self.set_opt_steps(new_state, terminal_state, old_opt_steps + len(states_queue) - index_best)
        if (new_opt_steps == old_opt_steps):
            index_best = len(states_queue)
        return states_queue, traj_steps, index_best, old_opt_steps
        
    # adds the new terminal state to dict of terminal states, and updates optimal_steps
    def add_to_terminal(self, terminal_state):
        self.terminal_states[terminal_state] = self.index
        self.index += 1
        new_shape = list(self.optimal_steps.shape)
        new_shape[-1] += 1  # Increase the last dimension by 1
        new_optimal_steps = np.zeros(new_shape)
        new_optimal_steps[:, :, :-1] = self.optimal_steps
        self.optimal_steps = new_optimal_steps
        self.default_legibility = 1 / len(self.terminal_states)
        return self.index - 1

    def get_default_legib(self):
        return self.default_legibility
    
    # returns a legibility score that is not normalized
    # does not account for TIME (earlier, more legible, etc.)
    def get_legibility_score(self, state, action_index, terminal_state, num_steps):
        if (self.feedback_table[state][action_index] == terminal_state or terminal_state == None):
            return 1, True
        elif (self.get_feedback(state, action_index) == None):
            return -1, False
        legibility = 0
        denom = 0
        for end_goal in self.terminal_states:
            prob_current_goal = self.default_legibility
            new_state = self.get_feedback(state, action_index)
            # make sure the feedback state is not a terminal state. if so, check if the the opt steps array from that steps is not 0. if it is 0, we can't calculate and return false
            if (self.get_opt_steps(new_state, end_goal) == 0):
                return -1, True
            numerator = np.exp(-num_steps - 1 - self.get_opt_steps(new_state, end_goal)) / np.exp(-self.get_opt_from_start(end_goal))
            denom += (numerator * prob_current_goal)
            if (end_goal == terminal_state):
                legibility = numerator * prob_current_goal
        return legibility / denom, True

