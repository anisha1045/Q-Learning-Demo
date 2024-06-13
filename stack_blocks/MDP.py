import numpy as np
import random as rm
import task
import state

class Environment:
    def __init__(self):
        self.states = [state.State([[0, 0, 0], [0, 0, 0]], [task.Action.up, task.Action.down], reward = -1),
                state.State([[0, 0, 0], [0, 0, 0]], [1, 4], reward = -1),
                state.State([[0, 0, 0], [0, 0, 0]], reward = 10), 
                state.State([[0, 0, 0], [0, 0, 0]], [3, 5], reward = -1),
                state.State([[0, 0, 0], [0, 0, 0]], reward = 10)] 
    
    def step(self, cur_state, action):
        next_state= action.do(self.states[cur_state])
        rew = next_state.reward
        is_terminal = next_state.is_terminal
        return next_state, rew, is_terminal

class QTablePolicy:
    def __init__(self, env, total_episodes=10):
        self._total_episods = total_episodes
        self.qtable = []

    def get_action(self, state):
        action_index = np.argmax(self.qtable[state.index])
        return self.env.actions[action_index]
    
    def update(self, state, action, next_state, reward)
        self.qtable[] += ..


class DQNPolicy:


class MDP:
    def __init__(self, states) -> None:
        self.actions = [ (a.name, a.item) for a in task.Action.all()] #[("up", 0), ("right", 0) , ("up", 1), ("left", 1) , ("down", 0) , ("down", 1)]
        self.states = states
        self.initial_state = states[0]
        self.q_table = np.zeros((len(states), len(self.actions)))
        self.terminal_states = [2,4]
        self.total_episodes = 10
        self.steps_per_episode = 10
        self.exploration_rate = 0.7
        self.exploration_decay = 0.01
        self.discount_factor = 0.9
        self.learning_rate = 0.7
        self.end_episode = False

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
    

def run_task(env, init_state, policy):
    done = False
    state = init_state
    while not done:
        action = policy.get_action(state)
        next_state, reward, done = env.do_action(state, action)
        policy.update(next_state, reward)


    '''def get_state_index(self, state):
        for i in range(len(self.states)):
            if (self.states[i] == state):
                return i
        return -1'''
    
def main(self):
    for episode in range(self.total_episodes):
        current_state_index = 0
        print("Episode: ", episode)    
        episode_reward = 0
        num_steps = 0
        for step in range(self.steps_per_episode):
                num_steps += 1
                #state_index = self.get_state_index(current_state)
                state_index = current_state_index
                print("Current state index: ", current_state_index)
                new_state_index, action_index = self.choose_action(state_index)
                print("New state index: ", new_state_index)
                new_state = self.states[new_state_index]
                #print("New state: ",new_state)
                current_reward = new_state.reward
                episode_reward += current_reward
                #print("Current reward: ", current_reward
                self.q_table[state_index, action_index] = self.q_table[state_index, action_index] * \
                    (1 - self.learning_rate) + self.learning_rate * (current_reward + self.discount_factor * \
                    np.max(self.q_table[new_state_index, :]))
                if new_state_index in self.terminal_states:
                    print("BREAK")
                    #if (self.end_episode):
                        #self.arm_import.open_gripper()
                    break
                current_state_index = new_state_index
                print("===================================")
        print("||||||||||||||||||||||||||||||||||")
        
        
        self.exploration_rate *= (1 - self.exploration_decay)
            
    print(self.q_table)
        