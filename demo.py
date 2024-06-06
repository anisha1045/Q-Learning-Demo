import numpy as np
import grid
import random as rm

actions = {0:"up", 1:"down", 2:"left", 3:"right"}
q_table = np.zeros((3*3, len(actions)))
states = []
total_rewards = []

for i in range(grid.grid_dim):
    for j in range(grid.grid_dim):
        states.append([i, j])

rewards = np.zeros((3,3))
rewards[2,2] = 10
terminal_state = grid.terminal_state
total_episodes = 1
steps_per_episode = 10
exploration_rate = 0.7
exploration_decay = 0.05
discount_factor = 0.9
learning_rate = 0.7

def check_valid(state_index, action_index):
    state = states[state_index]
    
    # get state from state index
    # if state is on edge and we chose randomly, make sure we move legally


def choose_action(state_index):
    check_explore = rm.uniform(0, 1)
    # make safeties to make sure we dont go out of bounds
    if (check_explore > exploration_rate):
        word_index = rm.randint(0, 3)
        word_index = check_valid(state_index, word_index)
    else:
        word_index = np.argmax(q_table[state_index][:])
    print(actions[word_index])
    return getattr(grid, actions[word_index])(), word_index
         
def get_state_index(state):
    for i in range(len(states)):
        if (states[i] == state):
            return i
    return -1
    
for episode in range(total_episodes):
    current_state = grid.reset()
    episode_reward = 0
    num_steps = 0
    for step in range(steps_per_episode):
            num_steps += 1
            state_index = get_state_index(current_state)
            current_state, action_index = choose_action(state_index)
            print(current_state)
            next_state_index = get_state_index(current_state)
            if current_state == terminal_state:
                print("BREAK")
                break
            else:
                current_reward = rewards[current_state[0]][current_state[1]]
                episode_reward += current_reward
                print(current_reward)
                q_table[state_index, action_index] = q_table[state_index, action_index] * \
                (1 - learning_rate) + learning_rate * (current_reward + discount_factor * \
                np.max(q_table[next_state_index, :]))
            print("===================================")
    print("||||||||||||||||||||||||||||||||||")
    
    
    exploration_rate *= (1 - exploration_decay)
    total_rewards.append(episode_reward / num_steps) 
        
print(q_table)