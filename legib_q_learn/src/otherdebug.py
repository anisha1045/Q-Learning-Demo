import matplotlib.pyplot as plt

class GraphMaker:

    def __init__(self, num_eps, data_points):
        # Orig data
        self.x = [num_eps * i / data_points for i in range(data_points)]
        self.y = [0, 1.34, 4.37, 5.29, 5.4, 6.21]

        # Mod data
        self.x1 = [num_eps * i / data_points for i in range(data_points)]
        self.y2 = [0, 3.26, 3.91, 3.59, 3.16, 4.1]

    def make_graph(self):
        # Plotting the line graph
        plt.plot(self.x, self.y, label='Original', color='orange', linestyle='-', marker='o')
        plt.plot(self.x1, self.y2, label='Modified', color='pink', linestyle='-', marker='o')

        # Adding labels and title
        plt.xlabel('Number of Episodes')
        plt.ylabel('Average Reward')
        plt.title('Learning Efficiency For Original vs Modified Q Policy')

        # Adding a legend
        plt.legend()

        # Displaying the plot
        plt.show()

    graph = GraphMaker(50, 5)