import action 
'''
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

    def execute(self):
        return self._do()

    # Decorators to create Action instances with specific behaviors
    @Action.make()
    def up():
        print("Moving up")
        return 1

    @Action.make()
    def right():
        print("Moving right")
        return 2

    @Action.make()
    def left():
        print("Moving left")
        return 4

    @Action.make()
    def down():
        print("Moving down")
        return 0
    
class Action:
    ALL = []
    def __init__(self, name):
        self._name = name
        self._do = behavior
        setattr(Action, name, self)
    
    @classmethod
    def make(cls, *args, **kwargs):
        def make_action(behavior):
            return cls(behavior, *args, **kwargs)
        return make_action
    
    def execute(self):
        return self._do()

    @property
    def name(self):
        return self._name
    
    @property
    def item(self):
        return self._item

    @Action.make()
    def up_0():
        print("Moving up")
        return 1

    @Action.make()
    def up_1():
        print("Moving up")
        return 3

    @Action.make()
    def right():
        print("Moving right")
        return 2

    @Action.make()
    def left():
        print("Moving left")
        return 4

    @Action.make()
    def down():
        print("Moving down")
        return 0
'''

'''action4 = action.Action.down
print(action4.name)  # Output: down
action4.execute() '''
#Action = Action()
print(action.Action.ALL)
for thing in action.Action.ALL:
    print(thing.execute())
'''
class Action:
    ALL = []
    def __init__(self, name):
        self.name = name
        Action.ALL.append(self)

    def execute(self):
        return getattr(self, self.name)
    
    def up_0():
        print("Moving up")
        return 1
    
    def up_1():
        print("Moving up")
        return 3

    def right():
        print("Moving right")
        return 2

    def left():
        print("Moving left")
        return 4

    def down():
        print("Moving down")
        return 0
    
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

    def execute(self):
        return self._do()

    # Decorators to create Action instances with specific behaviors
    @Action.make()
    def up():
        print("Moving up")
        return 1

    @Action.make()
    def right():
        print("Moving right")
        return 2

    @Action.make()
    def left():
        print("Moving left")
        return 4

    @Action.make()
    def down():
        print("Moving down")
        return 0
'''