import numpy as np
import random as rm
import robot
import task

class Environment:
    
    def __init__(self, arm, task):
        self.arm = arm
        self.task = task
        self.states = self.task.get_states()
        self.actions_length = self.task.get_actions_length()
        
    # returns num_steps, stop, episode_reward
    def step(self, num_steps, policy, episode_reward):
        num_steps += 1
        current_state = self.task.get_current_state()
        #print("Current state: ", current_state.to_string())
        new_state, action_index = policy.get_action(current_state, self.task, self.arm)
        #print("New state: ", new_state.to_string())
        current_reward = new_state.get_reward()
        episode_reward += current_reward
        #print("Current reward: ", current_reward)
        policy.update_q_table(current_state, new_state, current_reward, action_index)
        stop = False
        if new_state in self.task.terminal_states:
            stop = True
        self.task.set_current_state(new_state)
        return num_steps, stop, episode_reward

    def reset(self):
        self.arm.open_gripper()
        self.arm.home_arm()
        self.current_state = self.task.reset(self.arm)

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
                num_steps, stop, episode_reward = env.step(num_steps, self, episode_reward)
                if stop:
                    print("BREAK")
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
    
    def update_q_table(self, state, new_state, reward, action_index):
        # ASSUME THAT THE Q TABLE HAS AT LEAST ONE ENTRY
        if new_state not in self.q_table.keys(): 
            self.q_table[new_state] = np.zeros(len(self.q_table[0]))
        self.q_table[state][action_index] = self.q_table[state][action_index] * \
            (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * \
            np.max(self.q_table[new_state]))



        

if __name__=="__main__":
    #task = task.Task_Stack()
    print("Creating a task object of task move")
    task = task.Task_Move(3)
    env = Environment(robot.Robot(), task)
    current_policy = QTablePolicy(env.states, env.actions_length)
    current_policy.learn_task(env)
    
    
        

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