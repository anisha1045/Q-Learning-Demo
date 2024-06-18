class Action:
    ALL = []

    def __init__(self, behavior):
        self._name = behavior.__name__  # Use the function name as the action name
        self._do = behavior
        __class__.ALL.append(self)
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
# Task Stack Actions
class TaskStackActions(Action):
    ALL = []

    def __init__(self, behavior):
        self._name = behavior.__name__  # Use the function name as the action name
        self._do = behavior
        __class__.ALL.append(self)
        setattr(Action, self._name, self)
    @classmethod
    def make_task_stack_action(cls):
        def make_action(behavior):
            return cls(behavior)
        return make_action

@TaskStackActions.make_task_stack_action()
def up_0(states, arm):
    print("Moving item0 up")
    return states[((1, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def up_1(states, arm):
    print("Moving item1 up")
    return states[((3, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def right(states, arm):
    print("Moving right")
    return states[((2, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def left(states, arm):
    print("Moving left")
    return states[((4, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def down(states, arm):
    print("Moving down")
    return states[((0, 0, 0), (0, 0, 0))]

# Task Move Actions
class TaskMoveActions(Action):
    ALL = []

    def __init__(self, behavior):
        self._name = behavior.__name__  # Use the function name as the action name
        self._do = behavior
        __class__.ALL.append(self)
        setattr(Action, self._name, self)

    @classmethod
    def make_task_move_action(cls):
        def make_action(behavior):
            return cls(behavior)
        return make_action

    def execute(self, states, state, arm):
        return self._do(states, state, arm)

@TaskMoveActions.make_task_move_action()
def up(states, state, arm):
    new_row = state.desc[0] - 1
    new_col = state.desc[1]
    print("UP")
    return states[(new_row, new_col)]

@TaskMoveActions.make_task_move_action()
def down(states, state, arm):
    print(state.desc)
    print(type(state.desc[0]))
    new_row = state.desc[0] + 1
    new_col = state.desc[1]
    print("DOWN")
    return states[(new_row, new_col)]

@TaskMoveActions.make_task_move_action()
def left(states, state, arm):
    new_row = state.desc[0]
    new_col = state.desc[1] - 1
    print("LEFT")
    return states[(new_row, new_col)]

@TaskMoveActions.make_task_move_action()
def right(states, state, arm):
    print(state.desc)
    print(type(state.desc[1]))
    new_row = state.desc[0]
    new_col = state.desc[1] + 1
    print("RIGHT")
    return states[(new_row, new_col)]
