import matplotlib.pyplot as plt
import numpy as np

class Grid():
    def __init__(self, grid_dim):
        grid = np.zeros((grid_dim, grid_dim))
        self.figure, self.axes = plt.subplots()
        self.axes.imshow(grid, cmap='Greys', extent = [-.5, grid_dim - .5, -.5, grid_dim - .5])
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.xticks(np.arange(-.5, grid_dim, 1))
        plt.yticks(np.arange(-.5, grid_dim, 1))
        '''self.axes.set_xticks()
        self.axes.set_yticks()'''

    def plot(self, tuple):
        self.axes.plot(tuple[0], tuple[1], market = 'o', color = 'm', linestyle = ':')

    def show_plot(self):
        plt.show()

bob = Grid(3)
bob.show_plot()