

class Action:
    ALL = []
    def __init__(self, behavior, name, item):
        self._name = name
        self._do = behavior
        self._item = item
        Action.ALL.append(self)
        setattr(Action, name, self)
    
    @classmethod
    def make(cls, *args, **kwargs):
        def make_action(behavior):
            return cls(behavior, *args, **kwargs)
        return make_action

    @property
    def name(self):
        return self._name
    
    @property
    def item(self):
        return self._item
    
    @property




# current_state is a state object passed in from MDP
# new and current locations are relative to the start state
# must return index numbers for the state
@Action.make("up", 0)
@Action.make("up", 1)
@Action.make("right", 0)
@Action.make("left", 1)
@Action.make("down", 0)
@Action.make("down", 1)
def up(item_num):
    if (item_num == 0):
        new_state = 1
    else:
        new_state = 3
    print("Moving up")
    return new_state

def down(item_num):
    print("Moving down")
    return 0

def left(item_num):
    print("Moving left")
    return 4

def right(item_num):
    print("Moving right")
    return 2

def main():
    distance_delta = .02
    
    print("Main")
    #world = MDP.MDP(states)
    #world.main()
    

if __name__ == "__main__":
    main()
    

'''
        # creates a list of the number of items needed for the task
        for m in range(self.num_items):
            self.items.append(item.Item(m, self.distance_delta))
        self.possible_states = {}
        # creates a list of possible states
        for i in range(self.height):
            for j in range(self.width):
                for item in range(self.items):
                    new_state = state.State(i)
                    coordinates = [[x + j * distance_delta, y, z + i * distance_delta],[x + j * distance_delta, y, z + i * distance_delta]]
                    self.possible_states[new_state] = coordinates
            # TO DO: figure out what to pass in (probably the ID)
        
            
    # moves the item to a valid location and returns a new state
    def move(self, item_num, dir, possible_states):
        current_location = self.locations[item_num][1]
        new_item_location = self.locations[item_num][0].getattr(dir)(current_location)
        # new_locations is all item locations and id for the new state
        new_locations = self.locations
        new_locations[item_num] = new_item_location
        # if the new state is not a possible state, return the current state
        if (possible_states.contains(new_item_location)):
            return possible_states[new_item_location]
        else:
            return self

        def get_new_state(self, item_num, new_item_location):
        # new_locations is all item locations and id for the new state
        new_locations = self.locations
        new_locations[item_num] = new_item_location
        # if the new state is not a possible state, return the current state
        if (self.possible_states.contains(new_item_location)):
            return self.possible_states[new_item_location]
        else:
            return self'''