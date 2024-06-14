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

    def execute(self, arm):
        return self._do(arm)

# Decorators to create Action instances with specific behaviors

@Action.make()
def up_0(arm):
      #arm.goto_cartesian_pose(x,y,z) # go to item0 
      #arm.goto_cartesian_pose(x,y,z) # pick up item0
      print("Moving item0 up")
      return 1
  
@Action.make()
def up_1(arm):
    #arm.goto_cartesian_pose(x,y,z) # go to item1
    #arm.goto_cartesian_pose(x,y,z) # pick up item1
    print("Moving item1 up")
    return 3

@Action.make()
def right(arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving right")
    return 2

@Action.make()
def left(arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving left")
    return 4

@Action.make()
def down(arm):
    #arm.goto_cartesian_pose(x,y,z)
    print("Moving down")
    return 0

