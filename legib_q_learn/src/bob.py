import matplotlib.pyplot as plt
import numpy as np

# Define grid size
grid_size = (10, 10)

# Create a blank grid
grid = np.zeros(grid_size)

# Define a trajectory (list of (x, y) tuples)
trajectory = [(0, 0), (1, 2), (2, 4), (3, 6), (4, 7), (5, 8), (6, 8), (7, 9), (8, 9), (9, 9)]

# Plot the grid
fig, ax = plt.subplots()
ax.imshow(grid, cmap='Greys', extent=[-0.5, grid_size[1]-0.5, -0.5, grid_size[0]-0.5])

# Set major ticks at the center of each cell
ax.set_xticks(np.arange(grid_size[1]))
ax.set_yticks(np.arange(grid_size[0]))

# Extract x and y coordinates from the trajectory
x_coords, y_coords = zip(*trajectory)

# Plot the trajectory
ax.plot(x_coords, y_coords, marker='o', color='red', linestyle='-')

# Optionally, annotate the points
for (x, y) in trajectory:
    ax.text(x, y, f'({x},{y})', ha='right', va='bottom', color='blue')

# Show the plot with grid lines
ax.set_xticks(np.arange(-0.5, grid_size[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, grid_size[0], 1), minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

plt.gca().invert_yaxis()  # Invert the y-axis to match typical grid orientation
plt.show()