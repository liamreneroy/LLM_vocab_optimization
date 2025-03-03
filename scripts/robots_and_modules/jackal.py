import sys
import numpy as np
import random
from robots_and_modules.helper_functions import maybe_include, create_state_dict


class Robot:
    def __init__(self, set_of_states):
        # USER TUNED: ROBOT CHARACTERISTICS
        self.form_factor = 'rover-shaped' # dog-shaped quadruped, humanoid, etc.
        self.communication_modality = 'audio beeps' # locomotion, body pose, audio beeps etc.
        
        # USER TUNED: PARAMETER DESCRIPTIONS
        # Descriptions of each parameter. Note "" is the default description.
        self.parameter_descriptions = {             
            "Beats Per Loop": ["The robot beeps slowly 1 time per second.", "The robot beeps at a normal speed 2 times per second.", "The robot beeps rapidly 4 times per second."],
            "Pitch Bend": ["The pitch of the robot's beeps bend with a downward inflection.", "The pitch of the robot's beeps remains monotone.", "The pitch of the robot's beeps bend with an upwards inflection."],
            "Gain": ["The robot's beeps are played at a very quiet volume.", "The robot's beeps are played at a normal volume.", "The robot's beeps are played at a very loud volume."],
            "Distortion": ["The robot's beeps are clean with no distortion.", "The robot's beeps are mildly distorted.", "The robot's beeps are highly distorted and sharp sounding."]
            }

        # USER TUNED: INDECES OF PARAMETER DEFAULTS
        self.parameter_defaults = {             
            "Beats Per Loop": 1,
            "Pitch Bend": 1,
            "Gain": 1,
            "Distortion": 0
            }


        # PASSIVE PARAMETERS
        self.parameter_ranges = {          # Number of values for each parameter          
            param: len(descriptions) for param, descriptions in self.parameter_descriptions.items()
        }
        

        self.action_space_shape = tuple(self.parameter_ranges.values())         # Shape of action space
        self.action_space = np.empty(self.action_space_shape, dtype=object)     # Initialize action space
        
        # Populate the array with fresh dictionary instances
        for index, _ in np.ndenumerate(self.action_space):                      # Creates a unique dictionary at each index
            self.action_space[index] = create_state_dict(set_of_states)         # of the action space array to store state counts

        # Initialize active parameters array of zeros
        self.active_parameters = np.zeros(len(self.parameter_ranges))


    def set_active_parameter(self, value_indices):
        """Sets the values for all parameters at once
        
        Args:
            value_indices (list or numpy.ndarray): Array of indices for each parameter value, in order
        """
        value_indices = np.array(value_indices)
        
        if value_indices.shape[0] != len(self.active_parameters):
            raise ValueError(f"Expected {len(self.active_parameters)} values but got {value_indices.shape[0]}")
            
        for param_idx, value_idx in enumerate(value_indices):
            param_name = list(self.parameter_ranges.keys())[param_idx]
            if value_idx < 0 or value_idx >= self.parameter_ranges[param_name]:
                raise ValueError(f"Value index {value_idx} out of range for parameter {param_name}")
                
        self.active_parameters = value_indices.copy()



    def generate_description(self, omission_probability=0.5):
        """Generates a description of active parameters with random omissions"""

        # USER TUNED: Adjust index of non-default descriptions to generate a dictionary of strings for each parameter
        parameter_strings = {
            "Beats Per Loop": maybe_include(omission_probability, self.parameter_descriptions["Beats Per Loop"][0] if self.active_parameters[0] == 0 else self.parameter_descriptions["Beats Per Loop"][1] if self.active_parameters[0] == 1 else self.parameter_descriptions["Beats Per Loop"][2] if self.active_parameters[0] == 2 else ""),
            "Pitch Bend": maybe_include(omission_probability, self.parameter_descriptions["Pitch Bend"][0] if self.active_parameters[1] == 0 else self.parameter_descriptions["Pitch Bend"][1] if self.active_parameters[1] == 1 else self.parameter_descriptions["Pitch Bend"][2] if self.active_parameters[1] == 2 else ""),
            "Gain": maybe_include(omission_probability, self.parameter_descriptions["Gain"][0] if self.active_parameters[2] == 0 else self.parameter_descriptions["Gain"][1] if self.active_parameters[2] == 1 else self.parameter_descriptions["Gain"][2] if self.active_parameters[2] == 2 else ""),
            "Distortion": maybe_include(omission_probability, self.parameter_descriptions["Distortion"][0] if self.active_parameters[3] == 0 else self.parameter_descriptions["Distortion"][1] if self.active_parameters[3] == 1 else self.parameter_descriptions["Distortion"][2] if self.active_parameters[3] == 2 else "")
        }

        ### Return the joined string after omission step
        non_empty_strings = [s for s in parameter_strings.values() if s]
        
        if not non_empty_strings:
            return "The robot does nothing."
        else:
            # Simply join all strings with spaces
            return " ".join(non_empty_strings)


    # Class Getters
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
    
    def get_parameter_names(self):
        """Returns list of parameter names in order they appear in action space"""
        return list(self.parameter_ranges.keys())



### To run the test, run the script with the argument "test":   python3 scripts/go1_obj.py test
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "test":
    ###  Test setting parameters and generating description
    test_values = [1, 1, 2, 2]  # Example values within range for each parameter
    test_omission_probability = 0.0
    test_set_of_states = [
            "S01: [Processing, The robot is calculating it's navigation route to the delivery destination.]",
            "S02: [Navigating, The robot is navigating normally towards the delivery destination.]",
            "S03: [Danger, The robot is signaling for the user's attention due to a dangerous hazard.]",
            "S04: [Stuck, The robot is signaling for the user's attention as its wheel being stuck.]",
            "S05: [Accomplished, The robot is signaling that it has successfully reached the delivery destination.]",
            "S06: [Unsure, The robot's statr is unclear as it does not appear to be in any of the described states.]"
        ]

    robot = Robot(set_of_states=test_set_of_states)
    robot.set_active_parameter(test_values)

    print(f"\nGenerated description with {test_omission_probability*100}% omission probability and test values: {test_values}")
    description = robot.generate_description(test_omission_probability)

    print(f"\n{description}")

    # Print action space shape and action space
    print(f"\nAction space shape: {robot.get_action_space_shape()}")

    # index that dictionary and increment the count for second state in set_of_states
    before_update = robot.get_action_space()[tuple(test_values)].copy()
    robot.get_action_space()[tuple(test_values)]['S02'] += 1
    
    # Verify change before/after and print one of the action space dictionaries to verify they are unique
    print("\nBefore update dictionary at test values:\t", before_update)
    print("Updated dictionary at test values +1 for S02:\t", robot.get_action_space()[tuple(test_values)])
    print(f"Action space dictionary at [0, 0, 0, 0]:\t {robot.get_action_space()[0, 0, 0, 0]}")

    
