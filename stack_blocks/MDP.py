import numpy as np
import random as rm
import action
import state

class Environment:
    def __init__(self):
        self.actions = action.Action.ALL
        self.states = [state.State(actions = [0, 1], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions = [2, 4], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions =[], reward = 10, location=[[0, 0, 0], [0, 0, 0]]), 
                   state.State(actions = [3, 4], reward = -1, location=[[0, 0, 0], [0, 0, 0]]),
                   state.State(actions = [], reward = 10, location=[[0, 0, 0], [0, 0, 0]])]
        self.initial_state = 0
        self.current_state_index = 0
        self.terminal_states = [2, 4]

    # returns num_steps, stop, episode_reward
    def step(self, num_steps, policy, episode_reward):
        num_steps += 1
        #state_index = self.get_state_index(current_state)
        print("Current state index: ", self.current_state_index)
                # WE LEFT OFF HERE
        new_state_index, action_index = policy.get_action(self.current_state_index, self.states)
        print("New state index: ", new_state_index)
        new_state = self.states[new_state_index]
        #print("New state: ",new_state)
        current_reward = new_state.reward
        episode_reward += current_reward
        #print("Current reward: ", current_reward
        policy.update_q_table(self.current_state_index, action_index, new_state_index, current_reward)
        stop = False
        if new_state_index in self.terminal_states:
            print("BREAK")
            #CALL TO ROBOT CLASS
            stop = True
        self.current_state_index = new_state_index
        print("===================================")
        return num_steps, stop, episode_reward

    def reset(self):
        self.current_state_index = 0

class QTablePolicy:
    def __init__(self, num_states, num_actions, total_episodes=10):
        self._total_episodes = total_episodes
        self.q_table = np.zeros((num_states, num_actions))
        self.total_episodes = 10
        self.steps_per_episode = 10
        self.exploration_rate = 0.7
        self.exploration_decay = 0.01
        self.discount_factor = 0.9
        self.learning_rate = 0.7
        self.end_episode = False

    def learn_task(self, env):
        for episode in range(self.total_episodes):
            print("Episode: ", episode)    
            episode_reward = 0
            num_steps = 0
            env.reset()
            for step in range(self.steps_per_episode):
                num_steps, stop, episode_reward = env.step(num_steps, self, episode_reward)
                if stop:
                    print("BREAK")
                    break
            print("Episode reward: ", episode_reward)
            print("Num steps: ", num_steps)
        print("||||||||||||||||||||||||||||||||||")
        self.exploration_rate *= (1 - self.exploration_decay)
        print(self.q_table)
    
    def get_action(self, state_index, states):
        # returns the state number and action index
        # assuming states is a dict mapping state_index : state() objects
        check_explore = rm.uniform(0, 1)
        possible_actions = states[state_index].actions
        print("Possible actions", possible_actions)
        if (check_explore < self.exploration_rate):
            action_index = rm.choice(possible_actions)
        else:
            max_val = 0
            ind = 0
            index_of_highest = 0
            for action_index in possible_actions: 
                print("Q table val", self.q_table[state_index, action_index])
                if (max_val < self.q_table[state_index, action_index]):
                    max_val = self.q_table[state_index, action_index]
                    index_of_highest = ind
                ind += 1
            action_index = possible_actions[index_of_highest]
        new_state_index = action.Action.ALL[action_index].execute()
        return new_state_index, action_index
    
    def update_q_table(self, state_index, action_index, new_state_index, reward):
        print("State index", state_index)
        print("action index", action_index)
        self.q_table[state_index, action_index] = self.q_table[state_index, action_index] * \
            (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
            np.max(self.q_table[new_state_index, :]))


class MDP:

    def main(self):
        env = Environment()
        current_policy = QTablePolicy(len(env.states), len(env.actions))
        current_policy.learn_task(env)

mdp_object  = MDP()
mdp_object.main()
    
    
        

''' Old Functions:

    # returns the state number and action index
    def choose_action(self, state_index):
        # assuming states is a dict mapping state_index : state() objects
        check_explore = rm.uniform(0, 1)
        possible_actions = self.states[state_index].actions
        print("Possible actions",possible_actions)
        if (check_explore < self.exploration_rate):
            action_choice = rm.choice(possible_actions)
        else:
            #print("else exploitation")
            q_vals_for_state = np.array([]) #np.empty(len(possible_actions))
            for action in possible_actions: 
                #print("Action: ", possible_actions[index])
                #print("Q table: ", q_table[state_index, possible_actions[index]])
                np.append(q_vals_for_state, self.q_table[state_index, action])
            #print("Actions For State: ", q_vals_for_state)
            index_of_highest = np.argmax(q_vals_for_state)
            # print(index_of_highest)
            action_choice = possible_actions[index_of_highest]
        action_index = action_choice
        #print("Action selected: ", actions[action_index])
        action = task.Action.ALL[action_index]
        result = action.do(state_index)
        return result, action_index #getattr(task, self.actions[action_index][0])(self.actions[action_index][1]), action_index

            # returns the state number and action index
    def choose_action(self, state_index):
        # assuming states is a dict mapping state_index : state() objects
        check_explore = rm.uniform(0, 1)
        possible_actions = self.states[state_index].actions
        print("Possible actions",possible_actions)
        if (check_explore < self.exploration_rate):
            action_choice = rm.choice(possible_actions)
        else:
            #print("else exploitation")
            q_vals_for_state = np.array([]) #np.empty(len(possible_actions))
            for action in possible_actions: 
                #print("Action: ", possible_actions[index])
                #print("Q table: ", q_table[state_index, possible_actions[index]])
                np.append(q_vals_for_state, self.q_table[state_index, action])
            #print("Actions For State: ", q_vals_for_state)
            index_of_highest = np.argmax(q_vals_for_state)
            # print(index_of_highest)
            action_choice = possible_actions[index_of_highest]
        action_index = action_choice
        #print("Action selected: ", actions[action_index])
        action = task.Action.ALL[action_index]
        result = action.do(state_index)
        return result, action_index #getattr(task, self.actions[action_index][0])(self.actions[action_index][1]), action_index
'''