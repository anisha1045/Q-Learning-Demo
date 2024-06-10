## Q Learning Demo 

This code uses the [Armpy library](https://github.com/AABL-Lab/armpy) from [AABL Lab](https://aabl.cs.tufts.edu/):  which uses ROS 1 Noetic and the MOVEIT package.

#### Main files 

`demo.py`: Python file that runs the q learning algorithm implementation on the Gen3 lite robot (6 dof) for any size of grid

`gridtemplate.py` : Python class to create a grid of a specified dimension and control the robot's movements (up, down, left, right) 
