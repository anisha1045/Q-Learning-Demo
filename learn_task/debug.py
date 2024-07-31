import numpy as np
import random as rm
#import robot
import task
import policyshape
from abc import ABC, abstractmethod


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
        new_state, action_index = policy.get_action(current_state, self.task)
        #print("New state: ", new_state.to_string())
        current_reward = new_state.get_reward()
        episode_reward += current_reward
        stop, new = self.task.check_terminal(new_state)
        policy.update_q_table(current_state, new_state, current_reward, action_index, new)
        self.task.set_current_state(new_state)
        return num_steps, stop, episode_reward, new_state

    def terminal_state_cb(self):
        self.arm.open_gripper()
        self.arm.home_arm()
        pass

    def reset(self):
        self.current_state = self.task.ep_reset()
    
#class QTablePolicy(ABC):

    #def __init__(self): 
# Allows for multiple terminal states and implements policy shaping
class ModQTablePolicy:

    def __init__(self, states, actions_length, start, grid_dim, total_episodes = 10, steps_per_episode = 5, exploration_rate = 0.7, exploration_decay = 0.01, discount_factor = 0.9, learning_rate = 0.7):
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
        self.legib = policyshape.PolicyShape(states, actions_length, start, grid_dim)
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
        self.create_q_table()
        self.exploration_rate = .7
        for episode in range(self.total_episodes):   
            episode_reward = 0
            self.num_steps = 0
            env.reset()
            self.terminal_state = None
            states_queue = []
            current_state = env.task.get_initial_state()
            old_opt_steps = -1
            traj_steps = 0
            index_best = -1
            print("Initial state: ", self.legib.states[current_state])
            if (episode == self.total_episodes - 1):
                env.task.change_last_episode()
            # choose a terminal state if we have seen at least one before
            if (len(env.task.get_terminal_states()) >= 1):
                self.terminal_state = env.task.choose_terminal()
                self.q_table = self.q_tables[self.terminal_state]
                states_queue = []
                print("Chosen goal: ", self.legib.states[self.terminal_state])
                if (self.legib.get_opt_from_start(self.terminal_state) != 0):
                    old_opt_steps = self.legib.get_opt_from_start(self.terminal_state)
                    index_best = 0
            for step in range(self.steps_per_episode):
                self.num_steps, stop, episode_reward, new_state = env.step(self.num_steps, self, episode_reward)
                # add the state action pair to the q,
                states_queue.append(current_state)
                if stop:
                    self.terminal_state = new_state
                # runs only if we have a goal or if we've reached a goal
                if (self.terminal_state != None):
                    states_queue, traj_steps, index_best, old_opt_steps = self.legib.propagate_opt_steps(new_state, self.terminal_state, stop, states_queue, old_opt_steps, traj_steps, index_best)
                if stop:
                    break 
                current_state = new_state
                traj_steps += 1
            print(self.legib.optimal_steps)
            self.exploration_rate *= (1 - self.exploration_decay)
            print("===================================")
            print("Episode reward: ", episode_reward)
            print("Num steps: ", self.num_steps)
            self.num_steps = 0
        print("||||||||||||||||||||||||||||||||||")
        print(self.legib.optimal_steps)
        env.task.show_plot()
        self.print_q_tables()

    
    # here is where we implement policy shaping
    def get_action(self, state, task):
        # returns the state and action index
        check_explore = rm.uniform(0, 1)
        # assumes that possible_actions is a list of action indices corresponding to the 
        # actions list in task
        possible_actions = state.get_action_indices()
        # 2d array that stores probability of an action and whether the legibility for the new state can be calculated or not
        action_probs = []
        denom = 0
        min = current_index = 0
        feedback_options = []
        step_options = []
        default = self.legib.get_default_legib()
        for action_index in possible_actions: 
            # returns -1 as the score if unable to calculate; feedback_avail stores whether feedback for that state action pair is available
            # the legibility score is the 
            prob_action, feedback_avail = self.legib.get_legibility_score(state, action_index, self.terminal_state, self.num_steps)
            print("Feedback avail")
            print("Legibility score: ", prob_action)
            print("Action index: ", action_index)
            if (prob_action == -1):
                prob_action = default
                if (not feedback_avail):
                    feedback_options.append(action_index)
                elif (not feedback_options):
                    step_options.append(action_index)
            if (self.q_table[state][action_index] != 0):
                prob_action *= np.exp(self.q_table[state][action_index])
            denom += prob_action
            action_probs.append([prob_action, feedback_avail])
            if (prob_action < action_probs[min][0]):
                min = current_index
            current_index += 1
        all_same_prob = True
        # normalizing the probabilities
        for j in range(len(action_probs)):
            action_probs[j][0] /= denom
            if (action_probs[0][0] != action_probs[j][0]):
                all_same_prob = False
        exploit = False
        # when exploring, we prioritize never been there and unknown optimal steps, then low legibilities 
        if (check_explore < self.exploration_rate):
            print("EXPLORING")
            #action_index = rm.choice(possible_actions)
            #if we are exploring, we choose an action index based on the following priorities:
            # 1. there is no feedback state for the state action pair, 2. not all optimal steps are known for this pair
            # 3. legibility scores are low
            np.random.seed(10)
            if (feedback_options):
                print("choosing based on feedback")
                action_index = rm.choice(feedback_options)
            elif (step_options):
                print("choosing based on optimal steps")
                action_index = rm.choice(step_options)
            else:
                print("choosing based on min legib")
                num_action_probs = [item[0] for item in action_probs]
                print("ARG MAX: ", np.argmin(num_action_probs))
                action_index = possible_actions[np.argmin(num_action_probs)]
                #print("choosing randomly")
                #action_index = rm.choice(possible_actions)
        else:
            ''' the action probs do not seem to be in the right order
                could it be possible that the q table is not working properly'''
            exploit = True
            print("EXPLOITING")
            print(action_probs)
            if (all_same_prob):
                action_index = rm.choice(possible_actions)
            else: 
                num_action_probs = [item[0] for item in action_probs]
                print("ARG MAX: ", np.argmax(num_action_probs))
                action_index = possible_actions[np.argmax(num_action_probs)]
            print(possible_actions)
            print("CHOSEN ACTION INDEX: ", action_index)
        new_state, tuple = task.take_action(action_index)
        task.set_current_state(new_state)
        known_terminal = len(env.task.get_terminal_states())
        task.test.run_tests(exploit, tuple, self.num_steps - 1, self.terminal_state, known_terminal)
        print("New state: ", new_state.desc)
        return new_state, action_index

    def update_q_table(self, state, new_state, reward, action_index, new = False):
        ''' If we reach a new terminal state, make a new q table and do it
            If we reach a terminal state that is DIFFERENT from our current terminal state,
            set self.q table to be that one
            Then, we set the reward to be -1 for the other terminal states'''
        # ASSUME THAT THE Q TABLE HAS AT LEAST ONE ENTRY
        # if we are at an unknown terminal state and this is not the first terminal state, make a new q table for it
        # and add it to the dictionary of q tables 
        if (new == True):
            print("Action Index: ", action_index)
            # Add terminal state to the legibility object and initialize optimal steps table
            self.legib.add_to_terminal(new_state)

            # Creating new q tables 
            if (len(self.q_tables.keys()) != 0):
                new_q = self.create_q_table() 
                print("CREATING Q TABLE FOR NEW STATE: ", new_state.desc)
            self.q_tables[new_state] = self.q_table
        elif (new_state in self.q_tables and new_state != self.terminal_state):
            self.q_table = self.q_tables[new_state]
        # feedback_state is the new state reached after a state action pair - we use its legibility score as the feedback
        self.legib.update_feedback(state, action_index, new_state)
        self.q_table[state][action_index] = self.q_table[state][action_index] * (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
                np.max(self.q_table[new_state]))
        # We don't want the reward from a goal to interfere with the q table of another goal
        if (reward == 10):
            reward = -1
        # updating all q tables at the same time 
        for q_table in self.q_tables.values():
            if (id(q_table) != id(self.q_table)):
                q_table[state][action_index] = q_table[state][action_index] * \
                    (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
                    np.max(q_table[new_state]))
        
    # for debugging purposes
    def print_q_tables(self):
        for state_key in self.q_tables.keys():
            print("Q Table: ", state_key.desc)
            current_q = self.q_tables[state_key]
            for key in current_q.keys():
                    print("State ", self.legib.states[key],": ", current_q[key])

if __name__=="__main__":
    grid_dim = 3
    classic_task = task.Task_Many_Goals(grid_dim, (0, grid_dim // 2), [(grid_dim - 1, 0), (grid_dim - 1, grid_dim - 1)], True)
    behind_task = task.Task_Many_Goals(grid_dim, (0, 0), [(grid_dim - 2, grid_dim - 2), (grid_dim - 1, grid_dim - 1)], True)
    between_task = task.Task_Many_Goals(grid_dim, (grid_dim // 2, grid_dim // 2), [(0, 0), (grid_dim - 1, grid_dim - 1)], True)
    env = Environment(classic_task)
    mod_policy = ModQTablePolicy(env.states, env.actions_length, classic_task.get_initial_state(), classic_task.grid_dim)
    #orig_policy = OrigQTablePolicy(env.states, env.actions_length, task.get_initial_state(), task.grid_dim)
    for i in range(1):
        mod_policy.learn_task(env)
    classic_task.test.display_results()
    
