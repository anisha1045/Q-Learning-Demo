## Q Learning Demo 

This code uses the [Armpy library](https://github.com/AABL-Lab/armpy) from [AABL Lab](https://aabl.cs.tufts.edu/) which uses ROS 1 Noetic and the MOVEIT package.

### Learn Task

This folder allows for abstraction and creates a MDP for each task instead of hardcoding the task. 

`MDP.py` : The Python file that creates the Markov Decision Process and runs the Q Learning algorithm for the task by creating the environment, actions, and states. 

`armpy` : The module for connecting to the Gen3 Lite arm with 6 degrees of freedom.

`action.py` : A Python file for the class for Action that creates Actions object for each task.

`state.py` : A Python file for the class State that creates State objects for each task.

`task.py` : A Python file for the class Task that creates Task objects for each task.

`robot.py` : A Python file that initializes the armpy module to create an instance of the arm.

`debug.py` : A Python file that we used to debug our code.

`oldaction.py` : A Python file with our old code for actions that is no longer used.


### Move Cup

This folder moves a cup into a nxn (best done in 3x3) dimension grid with the task hardcoded in the code. 

`demo.py` : A Python file that helps run the Q Learning algorithm to move the cup.

`fakearm.py` : A Python file for the simulated version of our robot arm.

`gridtemplate.py` : A Python file for creating the grid and actions. 

`state.py` : A Python file that keeps track of all the states for the grid.

`task.py` : A Python file to make an Action class and make Action objects for the movement of the cup.

`test.py` : A Python file that allows us to connect to the robot and run various tests on it using the command line. 
