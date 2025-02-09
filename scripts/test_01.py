
import numpy as np
from helper_functions import create_state_dict

set_of_states = [
    "S01: [Waiting for Input, The robot is in standby mode waiting for a command from the user]",
    "S02: [Analyzing Object, The robot is analyzing a target object in front of it on the ground]", 
    "S03: [Found Object, The robot has found a target object in front of it on the ground]",
    "S04: [Needs Help, The robot is experiencing an error and needs help from the user]",
    "S05: [Confused, The robot is confused and unsure what to do]",
    "S06: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
    ]


# Desired shape
array_shape = (3, 3, 2, 3)

# Initialize the array with unique dictionary instances at each position
state_array = np.empty(array_shape, dtype=object)

# Populate the array with fresh dictionary instances
for index, _ in np.ndenumerate(state_array):
    state_array[index] = create_state_dict(set_of_states)


# Example: Increment 'S03' at index [1, 0, 0, 2]
before_update = state_array[1, 0, 0, 2].copy()
state_array[1, 0, 0, 2]['S03'] += 1

# Verify change
print("Before update dictionary at [1, 0, 0, 2]:", before_update)
print("Updated dictionary at [1, 0, 0, 2]:", state_array[1, 0, 0, 2])

# Show another dictionary element to confirm they are unique dictionaries
print("Dictionary at [0, 0, 0, 0]:", state_array[0, 0, 0, 0])
