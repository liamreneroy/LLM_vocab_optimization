import numpy as np
import random
from helper_functions import maybe_include


class Robot:
    def __init__(self):
        # USER TUNED: ROBOT CHARACTERISTICS
        self.form_factor = 'dog-shaped quadruped' # dog-shaped quadruped, humanoid, etc.
        self.communication_modality = 'body pose' # locomotion, body pose, audio beeps etc.
        
        # USER TUNED: PARAMETER DESCRIPTIONS
        # Descriptions of each parameter. Note "" is the default description.
        self.parameter_descriptions = {             
            "Body Tilt": ["The robot tilts its torso to the left", "", "The robot tilts its torso to the right"],
            "Body Lean": ["The robot leans its torso backwards", "", "The robot leans its torso forward"],
            "Body Height": ["The robot lowers its body to the ground", "", "The robot raises its torso as high as it can"],
            "Body Direction": ["The robot faces the user in the scene.", "The robot faces a nearby strawberry in the scene."],
            "Motion Velocity": ["The robot moves slowly to achieve this pose.", "", "The robot moves quickly to achieve this pose."],
            "Motion Smoothness": ["The robot's motion is smooth without any disturbances.", "The robot's motion is unsmooth and shaky."]
        }

        # PASSIVE PARAMETERS
        self.parameter_ranges = {          # Number of values for each parameter          
            param: len(descriptions) for param, descriptions in self.parameter_descriptions.items()
        }
        
        self.action_space_shape = tuple(self.parameter_ranges.values()) # Shape of action space
        self.action_space = np.zeros(self.action_space_shape)           # Initialize action space


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
            "Body Tilt": maybe_include(omission_probability, self.parameter_descriptions["Body Tilt"][0] if self.active_parameters[0] == "left" else self.parameter_descriptions["Body Tilt"][2] if self.active_parameters[0] == "right" else ""),
            "Body Lean": maybe_include(omission_probability, self.parameter_descriptions["Body Lean"][0] if self.active_parameters[1] == "backward" else self.parameter_descriptions["Body Lean"][2] if self.active_parameters[1] == "forward" else ""),
            "Body Height": maybe_include(omission_probability, self.parameter_descriptions["Body Height"][0] if self.active_parameters[2] == "low" else self.parameter_descriptions["Body Height"][2] if self.active_parameters[2] == "high" else ""),
            "Body Direction": maybe_include(omission_probability, self.parameter_descriptions["Body Direction"][1] if self.active_parameters[3] == "user" else self.parameter_descriptions["Body Direction"][2] if self.active_parameters[3] == "object" else ""),
            "Motion Velocity": maybe_include(omission_probability, self.parameter_descriptions["Motion Velocity"][0] if self.active_parameters[4] == "slow" else self.parameter_descriptions["Motion Velocity"][2] if self.active_parameters[4] == "fast" else ""),
            "Motion Smoothness": maybe_include(omission_probability, self.parameter_descriptions["Motion Smoothness"][1] if self.active_parameters[5] == "smooth" else self.parameter_descriptions["Motion Smoothness"][2] if self.active_parameters[5] == "shaky" else "")
        }
        

        ## FIX THIS BELOW LATER

        # Filter out None values and empty strings
        non_empty_strings = [s for s in parameter_strings.values() if s is not None and s != ""]
        
        # Format with commas and 'and' before last item
        if len(non_empty_strings) > 1:
            formatted_text = ", ".join(non_empty_strings[:-1]) + " and " + non_empty_strings[-1]
        elif len(non_empty_strings) == 1:
            formatted_text = non_empty_strings[0]
        else:
            formatted_text = ""
            
        return formatted_text





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


robot = Robot()
# Test getting parameter ranges
parameter_ranges = robot.get_parameter_ranges()

print("Parameter ranges:")

for param, range_vals in parameter_ranges.items():
    print(f"{param}: {range_vals}")

# Test setting parameters and generating description
test_values = [2, 2, 1, 1, 1, 1]  # Example values within range for each parameter
robot.set_active_parameter(test_values)

print("\nGenerated description with test values:")
description = robot.generate_description(omission_probability=0.5)
print(description)
