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
total_episodes = 200
steps_per_episode = 30
exploration_rate = 0.7
exploration_decay = 0.05
discount_factor = 0.9
learning_rate = 0.7

def get_possible_actions(state_index):
    state = states[state_index]
    possible_actions = [0, 1, 2, 3]
    if (state[0] == 0):
        # we can't move up
        possible_actions.remove(0)
    if (state[0] == 2):
        # we can't move down
        possible_actions.remove(1)
    if (state[1] == 0):
        # we can't move left
        possible_actions.remove(2)
    if (state[1] == 2):
        # we can't move right
        possible_actions.remove(3)
    return possible_actions
    # get state from state index
    # if state is on edge and we chose randomly, make sure we move legally


def choose_action(state_index):
    check_explore = rm.uniform(0, 1)
    # make safeties to make sure we dont go out of bounds
    possible_actions = get_possible_actions(state_index)
    if (check_explore < exploration_rate):
        action_index = rm.choice(possible_actions)
    else:
        #print("else exploitation")
        q_vals_for_state = np.empty(len(possible_actions))
        for index in range(len(possible_actions)): 
            #print("Action: ", possible_actions[index])
            #print("Q table: ", q_table[state_index, possible_actions[index]])
            q_vals_for_state[index] = q_table[state_index, possible_actions[index]]
        #print("Actions For State: ", q_vals_for_state)
        index_of_highest = np.argmax(q_vals_for_state)
        # print(index_of_highest)
        action_index = possible_actions[index_of_highest]
    #print("Action selected: ", actions[action_index])
    return getattr(grid, actions[action_index])(current_state), action_index
         
def get_state_index(state):
    for i in range(len(states)):
        if (states[i] == state):
            return i
    return -1
    
for episode in range(total_episodes):
    print("Episode: ", episode)
    current_state = grid.reset()
    episode_reward = 0
    num_steps = 0
    for step in range(steps_per_episode):
            num_steps += 1
            state_index = get_state_index(current_state)
            #print("Current state: ", current_state)
            new_state, action_index = choose_action(state_index)
            #print("New state: ",new_state)
            next_state_index = get_state_index(new_state)
            current_reward = rewards[new_state[0]][new_state[1]]
            episode_reward += current_reward
            #print("Current reward: ", current_reward)
            q_table[state_index, action_index] = q_table[state_index, action_index] * \
            (1 - learning_rate) + learning_rate * (current_reward + discount_factor * \
            np.max(q_table[next_state_index, :]))
            if new_state == terminal_state:
                print("BREAK")
                break
            current_state = new_state
            print("===================================")
    print("||||||||||||||||||||||||||||||||||")
    
    
    exploration_rate *= (1 - exploration_decay)
    total_rewards.append(episode_reward / num_steps) 
rewards_per_hundred = np.split(np.array(total_rewards), 20)
count = 10

print("********Average reward per thousand episodes********\n")
for r in rewards_per_hundred:
    print(count, ": ", str(sum(r/10)))
    count += 10
        
print(q_table)