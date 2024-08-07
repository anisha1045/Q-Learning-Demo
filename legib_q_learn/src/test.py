import numpy as np
import matplotlib.pyplot as plt
''' class Test that contains all of the tests
set np.seed to the same values and set the goals states to the same start positions so it can be replicated
for the same set of random seeds, run the test class which contains the different tests
create a test object within the task class, and call its main with each step to update the values stored in this test class

if currently exploiting:
    store the % of steps in the left vs right side of the graph and compare it to the position of the current goal
    estimate the number of goals the robot knows about based on the overall legibility - if low, estimate low, if high, estimate high
all the time:
    we still use the boolean for exploiting or not 
    check the average legibility of the resulting state when its exploring vs exploiting and store those values
    check the average distance to the end when exploring vs exploiting and store those values
the main will call all functions in the test class'''

class Test:
    
    def __init__(self, states, initial_state, terminal_states, grid_dim, actions, num_eps, num_learns):
        self.steps_left_side = 0
        self.steps_right_side = 0
        self.legib_explore = 0
        self.legib_exploit = 0
        self.steps_explore = 0
        self.steps_exploit = 0
        self.num_explore = 0
        self.num_exploit = 0
        self.initial_state = initial_state
        self.states = states
        self.num_eps = num_eps
        self.num_learns = num_learns
        self.avg_rewards = None
        self.data_points = 5
        if (num_eps > self.data_points):
            self.avg_rewards = np.zeros((self.data_points, 2))
        # stores the past number of known goals
        self.past_known = 0
        self.ep_all_known = 0
        # num known goals are the indices
        self.known_goals = [[0, 0, 0]]
        self.terminal_states = {}
        index = 0
        for terminal_state in terminal_states:
            # terminal_state is a tuple
            self.terminal_states[terminal_state] = index
            index += 1
            self.known_goals.append([0, 0, 0])
        self.actions = actions
        self.opt_steps = np.full((grid_dim, grid_dim, len(self.terminal_states)), -1)
        self.legib_table = np.zeros((grid_dim, grid_dim, len(self.terminal_states)))
        self.populate_opt_steps()
        # stores the real optimal steps for each state in the grid
        # calls get_legib to get the real legibility for each state in the grid

    def populate_opt_steps(self):
        queue = []
        for terminal_state in self.terminal_states:
            queue.append(terminal_state)
            terminal_index = self.terminal_states[terminal_state]
            self.opt_steps[terminal_state[0]][terminal_state[1]][terminal_index] = 0
            while (len(queue) != 0):
                current_state = queue.pop(0)
                current_steps = self.opt_steps[current_state[0]][current_state[1]][terminal_index]
                # get the new state somehow
                for action_index in self.states[current_state].action_indices:
                    action = self.actions[action_index]
                    state = action.execute(self.states[current_state], 0)
                    # take action here maybe have something to do with task
                    if (self.opt_steps[state[0]][state[1]][terminal_index] == -1):
                        self.opt_steps[state[0]][state[1]][terminal_index] = current_steps + 1
                        queue.append(state)
        print(self.opt_steps)

    def get_legib(self, new_state, num_steps, terminal_state):
        legibility = 0
        denom = 0
        if (new_state in self.terminal_states):
            return 1
        for end_goal in self.terminal_states:
            prob_current_goal = 1 / len(self.terminal_states)
            terminal_index = self.terminal_states[end_goal]
            numerator = np.exp(-num_steps -self.opt_steps[new_state[0]][new_state[1]][terminal_index]) / np.exp(-self.opt_steps[self.initial_state[0]][self.initial_state[1]][terminal_index])
            denom += (numerator * prob_current_goal)
            if (end_goal == terminal_state.desc):
                legibility = prob_current_goal * numerator
        return legibility / denom

    def update_steps(self):
        pass

    def estimate_goals(self):
        pass 

    # question, when the new state is a terminal state should we add the 1 to the exploit/explore vals
    # DOESNT TAKE INTO ACCOUNT THE TIME 
    def update_avg_legib(self, exploit, new_state, terminal_state, current_legib, current_opt_steps):
        # TO DO: WHEN WE GET ALLTESTS WORKING, UPDATE THIS IN RUN_TESTS
        if (terminal_state != None):
            if (exploit):
                print("EXPLOITED!")
                self.legib_exploit += current_legib
                self.steps_exploit += current_opt_steps
                self.num_exploit += 1
            else:
                print("EXPLORED!")
                self.legib_explore += current_legib
                self.steps_explore += current_opt_steps
                self.num_explore += 1
            print("LEGIB'S STATE: ", new_state)
            print("LEGIB ADDED: ", current_legib)

    # only runs if exploit is true
    # only makes sense if there are 2 goals
    def update_known_goals(self, new_state, terminal_known, current_legib, current_opt_steps):
        self.known_goals[terminal_known][0] += current_legib
        self.known_goals[terminal_known][1] += current_opt_steps
        self.known_goals[terminal_known][2] += 1


    # new_state and terminal_state are tuples 
    def run_tests(self, exploit, new_state, num_steps, terminal_state, terminal_known):
        if (terminal_state != None):
            current_legib = self.get_legib(new_state, num_steps, terminal_state)
            current_opt_steps = self.opt_steps[new_state[0]][new_state[1]][self.terminal_states[terminal_state.desc]]
            if (exploit):
                self.update_known_goals(new_state, terminal_known, current_legib, current_opt_steps)
            self.update_avg_legib(exploit, new_state, terminal_state, current_legib, current_opt_steps)
    
    def learning_test(self, episode_reward, episode, terminal_known):
        # test for average episode at which all episodes are found
        if (terminal_known > self.past_known and terminal_known == len(self.terminal_states)):
            self.past_known = terminal_known
            self.ep_all_known += episode + 1
        # testing for reward efficiency 
        if (self.avg_rewards is not None):
            print("ADDING EPISODE REWARD TO AVG REWARDS: ", episode_reward)
            index = episode // (self.num_eps // self.data_points)
            self.avg_rewards[index][0] += episode_reward
            self.avg_rewards[index][1] += 1
        
    # resets the past known number of terminal states at the beginning of every learning phase
    def reset(self):
        self.past_known = 0
    def display_results(self):
        rewards = [0]
        for data_point in self.avg_rewards:
            print(data_point[0])
            print(data_point[1])
            data_point[0] /= data_point[1]
            rewards.append(data_point[0])
            print("Avg reward: ", data_point[0])
        print(rewards)
        # TO DO: change this so that only the num learns in which all goals were found are included
        print("AVERAGE EPISODE AT WHICH ALL GOALS KNOWN: ", self.ep_all_known / self.num_learns)
        print()
        print("LEGIBS AS KNOWN GOALS INCREASE: ")
        for index in range(len(self.known_goals)):
            print("Known Goals: ", index)
            if (index == 0):
                print("Average Legibility: N/A")
            elif (self.known_goals[index][1] != 0):
                print("Average Legibility: ", self.known_goals[index][0]/self.known_goals[index][2])
                print("Avg Opt Steps: ", self.known_goals[index][1]/self.known_goals[index][2])
            else: 
                print("Average Legibility: Unknown")
        print()
        print("EXPLORE VS EXPLOIT LEGIBILITIES: ")
        if (self.num_exploit != 0):
            print("Exploiting Legib Average: ", self.legib_exploit / self.num_exploit)
            print("Exploiting Steps Average: ", self.steps_exploit / self.num_exploit)
        else:
            print("Averages could not be calculated.")
        if (self.num_explore != 0):
            print("Exploring Legib Average: ", self.legib_explore / self.num_explore)
            print("Exploring Steps Average: ", self.steps_explore / self.num_explore)
        else:
            print("Averages could not be calculated.")





