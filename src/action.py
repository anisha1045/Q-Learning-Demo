import sub

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
    arm.goto_cartesian_pose(0.07, -0.15, -0.43)
    arm.close_gripper()
    arm.goto_cartesian_pose(0, 0, 0.07)
    return states[((1, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def up_1(states, arm):
    print("Moving item1 up")
    arm.goto_cartesian_pose(-0.13, -0.17, -0.44)
    arm.close_gripper()
    arm.goto_cartesian_pose(0, 0, 0.07)
    return states[((3, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def right(states, arm):
    print("Moving right")
    arm.goto_cartesian_pose(-0.19, 0, 0)
    return states[((2, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def left(states, arm):
    print("Moving left")
    arm.goto_cartesian_pose(0.19, 0, 0)
    return states[((4, 0, 0), (0, 0, 0))]

@TaskStackActions.make_task_stack_action()
def down(states, arm):
    print("Moving down")
    arm.goto_cartesian_pose(0, 0, -0.07)
    return states[((0, 0, 0), (0, 0, 0))]

# Task Move Actions
class TaskMoveActions(Action):
    ALL = []

    def __init__(self, behavior):
        self._name = behavior.__name__  # Use the function name as the action name
        self._do = behavior
        __class__.ALL.append(self)
        try:
            self.sub_object = sub.Color_Detect_Sub()
        except rospy.ROSInterruptException:
            pass
        setattr(Action, self._name, self)

    @classmethod
    def make_task_move_action(cls):
        def make_action(behavior):
            return cls(behavior)
        return make_action

    def execute(self, states, state, distance_delta, arm):
        self._do(distance_delta, arm)
        # the call to the following function returns a tuple in the form (row, col)
        return states[self.sub_object.get_pos()]

@TaskMoveActions.make_task_move_action()
def up(distance_delta, arm):
    print("UP")
    arm.goto_cartesian_pose(0, -distance_delta, 0)

@TaskMoveActions.make_task_move_action()
def down(distance_delta, arm):
    print("DOWN")
    arm.goto_cartesian_pose(0, distance_delta, 0)

@TaskMoveActions.make_task_move_action()
def left(distance_delta, arm):
    print("LEFT")
    arm.goto_cartesian_pose(distance_delta, 0, 0)

@TaskMoveActions.make_task_move_action()
def right(distance_delta,  arm):
    arm.goto_cartesian_pose(-distance_delta, 0, 0)
    print("RIGHT")
