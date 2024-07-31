import numpy as np
action_probs = [[0.1, True], [0.2, True], [0.3, True]]
# [[0.3333333333333333, False], [0.3333333333333333, False], [0.3333333333333333, False]]
unique_values, counts = np.unique([row[0] for row in action_probs], return_counts=True)
duplicates = unique_values[counts > 1]
if len(duplicates) > 0:
    # Get the smallest duplicate value
    smallest_duplicate = np.min(duplicates)
# Get the indices of this smallest duplicate value
smallest_duplicate_indices = np.where([row[0] for row in action_probs] == smallest_duplicate)[0]
print(f"Indices of the smallest duplicate value ({smallest_duplicate}):", smallest_duplicate_indices)