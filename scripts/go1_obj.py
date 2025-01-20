import numpy as np


class Robot:
    def __init__(self):
        self.form_factor = 'dog-shaped quadruped'
        self.communication_modality = 'body pose'  # locomotion, body pose, audio beeps etc.

        self.parameter_ranges = {
            "Body Tilt": 3,
            "Body Lean": 3,
            "Body Height": 3,
            "Body Direction": 2,
            "Motion Velocity": 3,
            "Motion Smoothness": 2,
            }

        self.action_space_shape = tuple(self.parameter_ranges.values())

        self.action_space = np.zeros(self.action_space_shape)

    def get_form_factor(self):
        return self.form_factor

    def get_communication_modality(self):
        return self.communication_modality

    def get_parameter_ranges(self):
        return self.parameter_ranges

    def get_action_space_shape(self):
        return self.action_space_shape

    def get_action_space(self):
        return self.action_space


robot = Robot()



## -------------------------------------
## How to Index the Action Space
## -------------------------------------

# # Access a specific combination of parameters
# value = array[1, 2, 0, 1, 2, 0]  # Example indices
# print("Value at index [1, 2, 0, 1, 2, 0]:", value)

# # Modify the value at a specific combination of parameters
# array[0, 0, 1, 0, 1, 1] = 42
# print("Updated value at index [0, 0, 1, 0, 1, 1]:", array[0, 0, 1, 0, 1, 1])


# # Access all combinations where Motion Smoothness = 1
# slice_example = array[:, :, :, :, :, 1]  # Motion Smoothness fixed at 1
# print("Values where Motion Smoothness = 1:\n", slice_example)

