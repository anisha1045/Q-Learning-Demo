class Action:
    ALL = []

    def __init__(self, behavior):
        self._name = behavior.__name__  # Use the function name as the action name
        self._do = behavior
        Action.ALL.append(self)
        setattr(Action, self._name, self)

    @classmethod
    def make(cls):
        def make_action(behavior):
            return cls(behavior)  # Create Action instance with the behavior (function)
        return make_action

    @property
    def name(self):
        return self._name

    def execute(self, states, arm):
        return self._do(states, arm)

# Decorators to create Action instances with specific behaviors

@Action.make()
def up_0(states, arm):
      #arm.goto_cartesian_pose(x,y,z) # go to item0 
      #arm.goto_cartesian_pose(x,y,z) # pick up item0
      print("Moving item0 up")
      return states[1]
  
@Action.make()
def up_1(states, arm):
    #arm.goto_cartesian_pose(x,y,z) # go to item1
    #arm.goto_cartesian_pose(x,y,z) # pick up item1
    print("Moving item1 up")
    return states[3]

@Action.make()
def right(states, arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving right")
    return states[2]

@Action.make()
def left(states, arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving left")
    return states[4]

@Action.make()
def down(states, arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving down")
    return states[0]

