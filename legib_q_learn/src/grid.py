import matplotlib.pyplot as plt
import numpy as np
import time

class Grid():
    def __init__(self, grid_dim, start_coord, show = True):
        grid = np.zeros((grid_dim, grid_dim))
        self.figure, self.axes = plt.subplots()
        self.axes.set_title("Environment")
        self.axes.imshow(grid, cmap='Greys', extent = [-.5, grid_dim - .5, -.5, grid_dim - .5])
        plt.gca().invert_yaxis()
        # major ticks are -.5 and so on
        self.axes.set_xticks(np.arange(-.5, grid_dim, 1))
        self.axes.set_yticks(np.arange(-.5, grid_dim, 1))
        self.axes.set_xticks(np.arange(0, grid_dim, 1), np.arange(0, grid_dim, 1), minor = True)
        self.axes.set_yticks(np.arange(0, grid_dim, 1), np.arange(0, grid_dim, 1), minor = True)
        self.axes.grid()
        self.axes.tick_params(axis = 'x', bottom = False, top = False, labelbottom = False, labeltop = False)
        self.axes.tick_params(axis = 'x', which = 'minor', bottom = False, top = False, labelbottom = False, labeltop = True)
        self.axes.tick_params(axis = 'y', left = False, labelleft = False)
        self.axes.tick_params(axis = 'y', which = 'minor', left = False, labelleft = True)
        self.reward_tuples = []
        self.start_coord = start_coord
        self.current_state = self.start_coord
        self.update = True
        plt.ion()

    def plot_reward(self, tuple):
        self.axes.plot(tuple[1], tuple[0], color = 'y', marker = '*', markersize = 10)
        self.reward_tuples.append(tuple)

    def plot_traj(self, tuple):
        self.axes.plot([self.current_state[1], tuple[1]], [self.current_state[0], tuple[0]], marker = "o", color = 'pink')
        self.axes.plot(tuple[1], tuple[0], marker = "o", color = "orange")
        if (tuple in self.reward_tuples):
            self.update = False
            self.current_state = self.start_coord
        else:
            self.current_state = tuple
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        time.sleep(.5)

    def show_plot(self):
        plt.show()

    def end(self):
        plt.ioff()
        plt.show()

# note: make sure you reset the grid after every episode