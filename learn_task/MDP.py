import numpy as np
import random as rm
#import robot
import task
import policyshape

''' Problems: q tables are not printing gasp and optimal steps table is ALL WRONG'''
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
    
class OrigQTablePolicy():
    # here, we still choose a goal, but we don't do anything with legibility
    def __init__(self, states, actions_length, total_episodes = 50, steps_per_episode = 15, exploration_rate = 0.7, exploration_decay = 0.05, discount_factor = 0.9, learning_rate = 0.7):
        self.q_table = {}
        self.q_tables = {}
        self.actions_length = actions_length
        print("ORIG TOTAL EPISODES: ", total_episodes)
        self.total_episodes = total_episodes
        self.steps_per_episode = steps_per_episode
        self.orig_exp_rate = self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.states = states
        self.num_steps = 0
        self.terminal_state = None

    def reset_q_object_info(self):
        self.q_table = {}
        self.q_tables = {}
        self.terminal_state = None
        self.exploration_rate = self.orig_exp_rate
        

    def create_q_table(self):
        new_q = {}
        for state in self.states.values():
            new_q[state] = np.zeros(self.actions_length)
        self.q_table = new_q
        return new_q

    # here is where we implement policy shaping
    def get_action(self, state, task):
        # returns the state and action index
        check_explore = rm.uniform(0, 1)
        # assumes that possible_actions is a list of action indices corresponding to the 
        # actions list in task
        possible_actions = state.get_action_indices()
        print("Possible actions", possible_actions)
        exploit = False
        if (check_explore < self.exploration_rate):            
            print("EXPLORING")
            action_index = rm.choice(possible_actions)
        else:
            exploit = True
            print("EXPLOITING")
            max_val = 0
            ind = 0
            index_of_highest = 0
            for action_index in possible_actions: 
                print("Q table val: ", self.q_table[state][action_index])
                if (max_val < self.q_table[state][action_index]):
                    max_val = self.q_table[state][action_index]
                    index_of_highest = ind
                ind += 1
            action_index = possible_actions[index_of_highest]
        print("CHOSEN ACTION INDEX: ", action_index)
        new_state, tuple = task.take_action(action_index)
        task.set_current_state(new_state)
        known_terminal = len(env.task.get_terminal_states())
        if (task.get_test_mode()):
            print("TEST MODE IS TRUE.")
            print("Num known: ", known_terminal)
            task.test.run_tests(exploit, tuple, self.num_steps - 1, self.terminal_state, known_terminal)
        print("New state: ", new_state.desc)
        return new_state, action_index
    
    def learn_task(self, env):
        self.reset_q_object_info()
        self.create_q_table()
        env.task.learn_reset()
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
            print("Initial state: ", current_state.desc)
            if (episode == self.total_episodes - 1):
                env.task.change_last_episode()
            # choose a terminal state if we have seen at least one before
            if (len(env.task.get_terminal_states()) >= 1):
                self.terminal_state = env.task.choose_terminal()
                self.q_table = self.q_tables[self.terminal_state]
                states_queue = []
                print("Chosen goal: ", self.terminal_state.desc)
            for step in range(self.steps_per_episode):
                self.num_steps, stop, episode_reward, new_state = env.step(self.num_steps, self, episode_reward)
                # add the state action pair to the q,
                states_queue.append(current_state)
                if stop:
                    break 
                current_state = new_state
                traj_steps += 1
            if (env.task.get_test_mode()):
                env.task.test.learning_test(episode_reward, episode, len(env.task.get_terminal_states()))
            self.exploration_rate *= (1 - self.exploration_decay)
            print("===================================")
            print("Episode reward: ", episode_reward)
            print("Num steps: ", self.num_steps)
            self.num_steps = 0
        print("||||||||||||||||||||||||||||||||||")
        if (not env.task.get_test_mode()):
            env.task.show_plot()
        print(len(env.task.get_terminal_states()))
        print("PRINTING Q TABLES")
        self.print_q_tables()

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
            # Creating new q tables 
            if (len(self.q_tables.keys()) != 0):
                self.create_q_table() 
                print("CREATING Q TABLE FOR NEW STATE: ", new_state.desc)
            self.q_tables[new_state] = self.q_table
        elif (new_state in self.q_tables and new_state != self.terminal_state):
            self.q_table = self.q_tables[new_state]
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
                    print("State ", key.desc,": ", current_q[key])

                    
# Allows for multiple terminal states and implements policy shaping
class ModQTablePolicy(OrigQTablePolicy):
    def __init__(self, states, actions_length, start, grid_dim, total_episodes = 50, steps_per_episode = 15, exploration_rate = 0.7, exploration_decay = 0.05, discount_factor = 0.9, learning_rate = 0.7):
        super().__init__(states, actions_length, total_episodes, steps_per_episode, exploration_rate, exploration_decay, discount_factor, learning_rate)
        self.legib = policyshape.PolicyShape(self.states, self.actions_length, start, grid_dim)

    def reset_q_object_info(self):
        self.legib.reset()
        super().reset_q_object_info()

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
            prob_action, feedback_avail = self.legib.get_legibility_score(state, action_index, self.terminal_state, self.num_steps)
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
        unique_values, counts = np.unique([row[0] for row in action_probs], return_counts=True)
        duplicates = unique_values[counts > 1]
        smallest_duplicate = -1
        smallest_duplicate_indices = None
        if len(duplicates) > 0:
            smallest_duplicate = np.min(duplicates)
            largest_duplicate = np.max(duplicates)
            # Get the indices of this smallest duplicate value
            smallest_duplicate_indices = np.where([row[0] for row in action_probs] == smallest_duplicate)[0]
            largest_duplicate_indices = np.where([row[0] for row in action_probs] == largest_duplicate)[0]
        # normalizing the probabilities
        for j in range(len(action_probs)):
            action_probs[j][0] /= denom
        print("Action probs: ", action_probs)
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
                if (len(duplicates) > 0):
                    action_index = possible_actions[rm.choice(smallest_duplicate_indices)]
                else:
                    num_action_probs = [item[0] for item in action_probs]
                    action_index = possible_actions[np.argmin(num_action_probs)]
        else:
            exploit = True
            print("EXPLOITING")
            if (len(duplicates) > 0):
                action_index = possible_actions[rm.choice(largest_duplicate_indices)]
            else: 
                num_action_probs = [item[0] for item in action_probs]
                action_index = possible_actions[np.argmax(num_action_probs)]
            print(possible_actions)
            print("CHOSEN ACTION INDEX: ", action_index)
        new_state, tuple = task.take_action(action_index)
        task.set_current_state(new_state)
        known_terminal = len(env.task.get_terminal_states())
        if (task.get_test_mode()):
            task.test.run_tests(exploit, tuple, self.num_steps - 1, self.terminal_state, known_terminal)
        print("New state: ", new_state.desc)
        return new_state, action_index
    

    def learn_task(self, env):
        # reset the q tables and the known terminal states 
        self.reset_q_object_info()
        self.create_q_table()
        env.task.learn_reset()
        for episode in range(self.total_episodes):   
            print("Total episodes: ", self.total_episodes)
            episode_reward = 0
            self.num_steps = 0
            env.reset()
            self.terminal_state = None
            states_queue = []
            current_state = env.task.get_initial_state()
            old_opt_steps = -1
            traj_steps = 0
            index_best = -1
            print("Exploration rate: ", self.exploration_rate)
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
            if (env.task.get_test_mode()):
                env.task.test.learning_test(episode_reward, episode, len(env.task.get_terminal_states()))
            self.exploration_rate *= (1 - self.exploration_decay)
            print("===================================")
            print("Episode reward: ", episode_reward)
            print("Num steps: ", self.num_steps)
            self.num_steps = 0
        print("||||||||||||||||||||||||||||||||||")
        print("Optimal steps table: ")
        print(self.legib.optimal_steps)
        if (not env.task.get_test_mode()):
            env.task.show_plot()
        print("PRINTING Q TABLES")
        self.print_q_tables()

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
                self.create_q_table() 
                print("CREATING Q TABLE FOR NEW STATE: ", new_state.desc)
            self.q_tables[new_state] = self.q_table
        elif (new_state in self.q_tables and new_state != self.terminal_state):
            self.q_table = self.q_tables[new_state]
        # feedback_state is the new state reached after a state action pair - we use its legibility score as the feedback
        self.legib.update_feedback(state, action_index, new_state)
        print("Feedback table updated.")
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


if __name__=="__main__":
    grid_dim = 3
    test_mode = True
    num_learns = 10
    num_episodes = 50
    #classic_task = task.Task_Many_Goals(grid_dim, (0, grid_dim // 2), [(grid_dim - 1, 0), (grid_dim - 1, grid_dim - 1)], num_episodes, num_learns, test_mode)
    #behind_task = task.Task_Many_Goals(grid_dim, (0, 0), [(grid_dim - 2, grid_dim - 2), (grid_dim - 1, grid_dim - 1)], num_episodes,  num_learns, test_mode)
    between_task = task.Task_Many_Goals(grid_dim, (grid_dim // 2, grid_dim // 2), [(0, 0), (grid_dim - 1, grid_dim - 1)], num_episodes, num_learns, test_mode)
    env = Environment(between_task)
    mod_policy = ModQTablePolicy(env.states, env.actions_length, between_task.get_initial_state(), between_task.grid_dim, num_episodes)
    orig_policy = OrigQTablePolicy(env.states, env.actions_length)
    for i in range(num_learns):
        #mod_policy.learn_task(env)
        orig_policy.learn_task(env)
    if (test_mode):
        between_task.test.display_results()
    
# LEFT TO DO: AVERAGE REWARD AT THE END OF EACH 10 EPISODES - GRAPH IT AND PUT IT IN A MATPLOTLIB 
# AVERAGE EPISODE AT WHICH ALL GOALS ARE FOUND (EASIER)
        # Problem: exploit legib average is about the same as explore legib average
        # reasons: choosing the action index for exploit is not working correctly or adding the legib and dividing is not working correctly