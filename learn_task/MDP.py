import numpy as np
import random as rm
#import robot
import task
'''ASK ELAINE: 
different options: 
if feedback can't be calculated, we either exploit as usual or just explore
SHOULD I DO A MINI Q LEARNING THING OR ONLY GIVE IT FEEDBACK WHEN THERE EXISTS FEEDBACK 

What should we do during exploitation when we don't have all of the legibilities for each action?
Should we exploit even if we have no legibility information? That's what this code does.'''

''' Problems: I'm not sure if optimal_steps is updating correctly. Check the index_best business. I think that's alright.
    When the first state has a value, then make it the old opt steps. This is messing things up with the index_best I think. '''


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
        print("New state: ", new_state.to_string())
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
        self.current_state = self.task.reset()

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

    def propagate_opt_steps(self, new_state, action_index, terminal_state, stop, states_queue):
        new_opt_steps = self.get_opt_steps(new_state, terminal_state)
        print("new_opt_steps ", new_opt_steps)
        # if new_opt_steps is known and (we don't know some the opt for earlier states or the new_opt is faster) or if we've reached the end
        if (((new_opt_steps != 0) and (old_opt_steps == -1 or new_opt_steps < old_opt_steps - traj_steps)) or stop):
            print("PROPAGATING BACKWARD")
            # go through the queue and update the values accordingly
            # this is the best optimal steps, and we are going to propagate info backwards
            traj_steps = 0
            traj_length = len(states_queue)
            for k in range(len(states_queue)):
                state = states_queue[k]
                opt_steps = self.legib.get_opt_steps(state, self.terminal_state)
                if (opt_steps == 0 or traj_length - k + new_opt_steps < opt_steps):
                    print("UPDATING: ", state.desc)
                    print("Opt steps: ", traj_length - k + new_opt_steps)
                    self.legib.set_opt_steps(state, self.terminal_state, traj_length - k + new_opt_steps)
            old_opt_steps = new_opt_steps
            index_best = len(states_queue) - 1
        # if we're at a state the opt steps is unknown and we have been to a known opt steps before, propagate info forwards 
        # maybe not making full use of the information if new_opt_steps is known but bigger than it should be but oh well
        elif ((new_opt_steps == 0 or new_opt_steps > old_opt_steps + len(states_queue) - 1 - index_best) and not stop and old_opt_steps != -1):
            print("PROPAGATING FORWARD.")
            print("UPDATING: ", state.desc)
            print("Opt steps: ", old_opt_steps + len(states_queue) - 1 - index_best)
            self.legib.set_opt_steps(state, self.terminal_state, old_opt_steps + len(states_queue) - 1 - index_best)

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


# Allows for multiple terminal states and implements policy shaping
class ModQTablePolicy:

    def __init__(self, states, actions_length, start, grid_dim, total_episodes = 5, steps_per_episode = 15, exploration_rate = 0.7, exploration_decay = 0.01, discount_factor = 0.9, learning_rate = 0.7):
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

    ''' PLAN: if opt steps for start != 0 then set old_opt_steps to it, otherwise set it to -1'''
    def learn_task(self, env):
        self.create_q_table()
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
                    new_opt_steps = self.legib.get_opt_steps(new_state, self.terminal_state)
                    print("new_opt_steps ", new_opt_steps)
                    # if new_opt_steps is known and (we don't know some the opt for earlier states or the new_opt is faster) or if we've reached the end
                    if (((new_opt_steps != 0) and (old_opt_steps == -1 or old_opt_steps + traj_steps > new_opt_steps)) or stop):
                        print("PROPAGATING BACKWARD")
                        # go through the queue and update the values accordingly
                        # this is the best optimal steps, and we are going to propagate info backwards
                        traj_steps = 0
                        traj_length = len(states_queue)
                        for k in range(len(states_queue)):
                            state = states_queue[k]
                            opt_steps = self.legib.get_opt_steps(state, self.terminal_state)
                            if (opt_steps == 0 or traj_length - k + new_opt_steps < opt_steps):
                                print("UPDATING: ", state.desc)
                                print("Opt steps: ", traj_length - k + new_opt_steps)
                                self.legib.set_opt_steps(state, self.terminal_state, traj_length - k + new_opt_steps)
                        old_opt_steps = new_opt_steps
                        index_best = len(states_queue) - 1
                    # if we're at a state the opt steps is unknown and we have been to a known opt steps before, propagate info forwards 
                    # maybe not making full use of the information if new_opt_steps is known but bigger than it should be but oh well
                    elif ((new_opt_steps == 0 or new_opt_steps > old_opt_steps + len(states_queue) - index_best) and not stop and old_opt_steps != -1):
                        print("PROPAGATING FORWARD.")
                        print("UPDATING: ", new_state.desc)
                        print("Old opt steps: ", old_opt_steps)
                        print("Length: ", len(states_queue))
                        print(states_queue)
                        print("Index_best: ", index_best)
                        print("Opt steps: ", old_opt_steps + len(states_queue) - index_best)
                        self.legib.set_opt_steps(new_state, self.terminal_state, old_opt_steps + len(states_queue) - index_best)
                    if (new_opt_steps == old_opt_steps):
                        index_best = len(states_queue)
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
            #print("Legibility score: ", prob_action)
            #print("Action index: ", action_index)
            if (prob_action == -1):
                prob_action = default
                if (not feedback_avail):
                    feedback_options.append(action_index)
                elif (not feedback_options):
                    step_options.append(action_index)

                    # HERE 
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
        # when exploring, we prioritize never been there and unknown optimal steps, then low legibilities 
        if (check_explore < self.exploration_rate):
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
                action_index = rm.choice(possible_actions)
                '''print("choosing based on the minimum legibility")
                action_index = possible_actions[min]
                if (all_same_prob):
                    action_index = rm.choice(possible_actions)'''
        else:
            if (all_same_prob):
                action_index = rm.choice(possible_actions)
            else: 
                action_index = possible_actions[np.argmax(action_probs[0])]
        new_state = task.take_action(self.states, action_index)
        task.set_current_state(new_state)
        print("New state: ", str(new_state))
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