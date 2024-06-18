
import random as rm
import numpy as np
import state
import task
import action

def get_action(state_index):
        
    action4 = Action.down
    print(action4.name)  # Output: down
    action4.execute()
        states = [state.State([[0, 0, 0], [0, 0, 0]], actions= [Action.up, Action.up], reward = -1),
                   state.State([[0, 0, 0], [0, 0, 0]], actions= [Action.right, Action.down], reward = -1),
                   state.State([[0, 0, 0], [0, 0, 0]], actions=[], reward = 10), 
                   state.State([[0, 0, 0], [0, 0, 0]], actions= [Action.left, Action.down], reward = -1),
                   state.State([[0, 0, 0], [0, 0, 0]],actions= [], reward = 10)] 

        q_table = [3][4]
        # TO DO: USE STATE OBJECT INSTEAD OF STATE INDEX
        # returns the state number and action index
        # assuming states is a dict mapping state_index : state() objects
        check_explore = rm.uniform(0, 1)
        possible_actions = states[state_index].actions
        print("Possible actions", possible_actions)
        if (check_explore < 0.07):
            action_choice = rm.choice(possible_actions)
        else:
            max_val = 0
            ind = 0
            index_of_highest = 0
            for action in np.nditer(possible_actions): 
                if (max_val < q_table[state_index, action]):
                    max_val = q_table[state_index, action]
                    index_of_highest = ind
                ind += 1
            action_choice = possible_actions[index_of_highest]
        action_index = action_choice
        #print("Action selected: ", actions[action_index])
        action = task.Action.ALL[action_index]
        result = action.do(state_index)
        return result, action_index #getattr(task, self.actions[action_index][0])(self.actions[action_index][1]), action_index
        #action_index = np.argmax(self.qtable[state.index])
        #return self.env.actions[action_index]

get_action(1)



