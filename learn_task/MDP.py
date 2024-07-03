import numpy as np
import random as rm
#import robot
import task
''' What we are trying to do: 
    Start by knowing nothing. Have an initial q table.
    Once we reach a terminal state, we assign that q table to that terminal state.
    From here on, we randomly choose which terminal state is our goal. Say we choose terminal state 1.
    We will explore and exploit. If we explore and end up in a different terminal state, then we update the q table based on that one.'''
'''ASK ELAINE: SHOULD I DO A MINI Q LEARNING THING OR ONLY GIVE IT FEEDBACK WHEN THERE EXISTS FEEDBACK 
SHOULD I CALCULATE THE LEGIBILITIES FOR ALL ACTION CHOICES BEFOREHAND, OR SHOULD I USE LEGIBILITY SCORES BASED ON OLD TRAJECTORIES
exploration based on iverse legibility 1 
when at a state that you dont know anything about, just explore2 
use mat plot lib to plot the line segments as it moves
use info from 1 q table for multile q tables 
Problem: what should we do during exploitation when we don't have all of the legibilities for each action?'''


class Environment:
    
    def __init__(self, task):
        #self.arm = arm
        self.task = task
        self.states = self.task.get_states()
        self.actions_length = self.task.get_actions_length()
        
    # returns num_steps, stop, episode_reward
    def step(self, num_steps, policy, episode_reward):
        num_steps += 1
        current_state = self.task.get_current_state()
        #print("Current state: ", current_state.to_string())
        new_state, action_index = policy.get_action(current_state, self.task)
        print("New state: ", new_state.to_string())
        current_reward = new_state.get_reward()
        episode_reward += current_reward
        print("Current reward: ", current_reward)
        stop, new = self.task.check_terminal(new_state)
        policy.update_q_table(current_state, new_state, current_reward, action_index, new)
        self.task.set_current_state(new_state)
        return num_steps, stop, episode_reward, new_state, action_index

    def terminal_state_cb(self):
        self.arm.open_gripper()
        self.arm.home_arm()
        pass

    def reset(self):
        self.current_state = self.task.reset()

''' 
    Before every action, use the feedback table to choose an action:
    Get legibility score for all actions using the feedback table which stores the resulting new states
    Normalize probability score for all actions
    Policy shaping
    After every action, if the feedback table is empty, put the new state in the feedback table.
    '''
# we should only be using policy shape object if we've been to a terminal state before
# TO DO: MAKE SURE OPTIMAL STEPS IS CORRECT, AND LEGIBILITY IS CORRECT 
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
        # OPTIMAL STEPS IS NOT CORRECT 
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

    # returns a legibility score that is not normalized
    # does not account for TIME (earlier, more legible, etc.)
    def get_legibility_score(self, state, action_index, terminal_state, num_steps):
        if (self.get_feedback(state, action_index) == None or terminal_state == None):
            if (terminal_state == None):
                print("terminal state was none")
            else:
                print("there was no feedback for this.")
            print("couldn't calculate")
            return self.default_legibility
        elif (self.feedback_table[state][action_index] == terminal_state):
            return 1
        legibility = 0
        denom = 0
        for end_goal in self.terminal_states:
            prob_current_goal = self.default_legibility
            new_state = self.get_feedback(state, action_index)
            numerator = np.exp(-num_steps - 1 - self.get_opt_steps(new_state, end_goal)) / np.exp(-self.get_opt_from_start(end_goal))
            denom += (numerator * prob_current_goal)
            if (end_goal == terminal_state):
                legibility = numerator * prob_current_goal
        print(self.optimal_steps)
        print("calculated legibility")
        return legibility / denom


# Allows for multiple terminal states and implements policy shaping
class ModQTablePolicy:

    def __init__(self, states, actions_length, start, grid_dim, total_episodes = 200, steps_per_episode = 20, exploration_rate = 0.7, exploration_decay = 0.01, discount_factor = 0.9, learning_rate = 0.7):
        self.q_table = {}
        self.q_tables = {}
        self.actions_length = actions_length
        self.total_episodes = total_episodes
        self.steps_per_episode = steps_per_episode
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.end_episode = False
        self.states = states
        self.num_steps = 0
        self.legib = PolicyShape(states, actions_length, start, grid_dim)
        self.terminal_state = None

    def create_q_table(self):
        new_q = {}
        for state in self.states.values():
            new_q[state] = np.zeros(self.actions_length)
        self.q_table = new_q
        return new_q

    def get_action_prob(self):
        pass

    def learn_task(self, env):
        print('CREATING INITIAL Q TABLE')
        self.create_q_table()
        for episode in range(self.total_episodes):
            print("Episode: ", episode)    
            episode_reward = 0
            self.num_steps = 0
            env.reset()
            self.terminal_state = None
            states_queue = []
            current_state = env.task.get_initial_state()
            print("Initial state: ", current_state)
            print(self.legib.states[current_state])
            # choose a terminal state if we have seen at least one before
            if (len(env.task.get_terminal_states()) >= 1):
                self.terminal_state = env.task.choose_terminal()
                self.q_table = self.q_tables[self.terminal_state]
                print(self.legib.states[self.terminal_state])
            for step in range(self.steps_per_episode):
                self.num_steps, stop, episode_reward, new_state, action_index = env.step(self.num_steps, self, episode_reward)
                # add the state action pair to the q,
                states_queue.append((current_state, action_index))
                if stop:
                    self.terminal_state = new_state
                    # unravel the stack and update the values accordingly
                    if (states_queue):
                        new_val = self.num_steps
                        while (len(states_queue) >= 1):
                            state_action_pair = states_queue.pop(0)
                            # feedback_state is the new state reached after a state action pair - we use its legibility score as the feedback
                            feedback_state = self.terminal_state
                            if (states_queue):
                                feedback_state = states_queue[0][0]
                            self.legib.update_feedback(state_action_pair[0], state_action_pair[1], feedback_state)
                            if (new_val < self.legib.get_opt_steps(state_action_pair[0], self.terminal_state) or self.legib.get_opt_steps(state_action_pair[0], self.terminal_state) == 0):
                                self.legib.set_opt_steps(state_action_pair[0], self.terminal_state, new_val)
                            new_val -= 1
                    print("break")
                    break
                current_state = new_state
            print("===================================")
            print("Episode reward: ", episode_reward)
            print("Num steps: ", self.num_steps)
            self.num_steps = 0
        print("||||||||||||||||||||||||||||||||||")
        self.exploration_rate *= (1 - self.exploration_decay)
        for state_key in self.q_tables.keys():
            print("Q Table: ", state_key.desc)
            current_q = self.q_tables[state_key]
            for i in range(len(self.states)):
                if (list(self.states.values())[i] in current_q.keys()):
                    print("State ", str(i),": ", current_q[list(self.states.values())[i]])
    
    # here is where we will implement policy shaping
    # NEEDS ACCESS TO STATE AND TERMINAL STEPS
    def get_action(self, state, task):
        # returns the state and action index
        check_explore = rm.uniform(0, 1)
        # assumes that possible_actions is a list of action indices corresponding to the 
        # actions list in task
        possible_actions = state.get_action_indices()
        if (check_explore < self.exploration_rate):
            action_index = rm.choice(possible_actions)
        else:
            print("Exploiting")
            action_probs = []
            denom = 0
            for action_index in possible_actions: 
                prob_action = self.legib.get_legibility_score(state, action_index, self.terminal_state, self.num_steps)
                print("Legibility score: ", prob_action)
                if (self.q_table[state][action_index] != 0):
                    prob_action *= abs(self.q_table[state][action_index])
                #print("Legibility score: ", self.legib.get_legibility_score(state, action_index, self.terminal_state, self.num_steps))
                denom += prob_action
                action_probs.append(prob_action)
            # normalizing the probabilities
            for j in range(len(action_probs)):
                action_probs[j] /= denom
            action_index = possible_actions[np.argmax(action_probs)]
        new_state = task.take_action(self.states, action_index)
        task.set_current_state(new_state)
        print("New state: ", str(new_state))
        return new_state, action_index

    def update_q_table(self, state, new_state, reward, action_index, new = False):
        # ASSUME THAT THE Q TABLE HAS AT LEAST ONE ENTRY
        # if we are at an unknown terminal state and this is not the first terminal state, make a new q table for it
        # and add it to the dictionary of q tables 
        if (new == True):
            print("New is true, we have reached a new terminal state.")
            # Add terminal state to the legibility object and initialize feedback table
            self.legib.add_to_terminal(new_state)

            # Creating new q tables 
            if (len(self.q_tables.keys()) != 0):
                new_q = self.create_q_table() 
                print("CREATING Q TABLE FOR NEW STATE: ", new_state.desc)
                self.print_q_table()
            self.q_tables[new_state] = self.q_table
        self.q_table[state][action_index] = self.q_table[state][action_index] * \
            (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
            np.max(self.q_table[new_state]))
        
    # for debugging purposes
    def print_q_table(self):
        for state in self.states.keys():
            print(state)
            print(self.q_table[self.states[state]])

if __name__=="__main__":
    task = task.Task_Many_Goals(5)
    env = Environment(task)
    current_policy = ModQTablePolicy(env.states, env.actions_length, task.get_initial_state(), task.grid_dim)
    current_policy.learn_task(env)
    
    
        

''' Unused Code:
class QTablePolicy:

    def __init__(self, states, actions_length, total_episodes = 10, steps_per_episode = 10, exploration_rate = 0.7, exploration_decay = 0.01, discount_factor = 0.9, learning_rate = 0.7):
        self.q_table = {}
        self.total_episodes = total_episodes
        self.steps_per_episode = steps_per_episode
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.end_episode = False
        self.states = states
        for state in states.values():
            self.q_table[state] = np.zeros(actions_length)

    def learn_task(self, env):
        for episode in range(self.total_episodes):
            print("Episode: ", episode)    
            episode_reward = 0
            num_steps = 0
            env.reset()
            for step in range(self.steps_per_episode):
                num_steps, stop, episode_reward, _, _ = env.step(num_steps, self, episode_reward)
                if stop:
                    self.terminal_state_cb()
                    break
            print("===================================")
            print("Episode reward: ", episode_reward)
            print("Num steps: ", num_steps)
        print("||||||||||||||||||||||||||||||||||")
        self.exploration_rate *= (1 - self.exploration_decay)
        for i in range(len(self.states)):
            if (list(self.states.values())[i] in self.q_table.keys()):
                print("State ", str(i),": ", self.q_table[list(self.states.values())[i]])
    
    def get_action(self, state, task, arm):
        # returns the state and action index
        check_explore = rm.uniform(0, 1)
        # assumes that possible_actions is a list of action indices corresponding to the 
        # actions list in task
        possible_actions = state.get_action_indices()
        if (check_explore < self.exploration_rate):
            action_index = rm.choice(possible_actions)
        else:
            max_val = 0
            ind = 0
            index_of_highest = 0
            for action_index in possible_actions: 
                if (max_val < self.q_table[state][action_index]):
                    max_val = self.q_table[state][action_index]
                    index_of_highest = ind
                ind += 1
            action_index = possible_actions[index_of_highest]
        new_state = task.take_action(self.states, action_index, arm)
        task.set_current_state(new_state)
        # print("New state: ", str(new_state))
        return new_state, action_index
    
    def update_q_table(self, state, new_state, reward, action_index, new = False):
        # WE AREN'T USING NEW HERE 
        # ASSUME THAT THE Q TABLE HAS AT LEAST ONE ENTRY
        if new_state not in self.q_table.keys(): 
            self.q_table[new_state] = np.zeros(len(self.q_table[0]))
        self.q_table[state][action_index] = self.q_table[state][action_index] * \
            (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
            np.max(self.q_table[new_state]))

'''