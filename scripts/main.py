# Imports
import sys
import numpy as np

# Default to go1_obj
robot_module = 'go1_obj'

# Only change to jackal if explicitly specified
if len(sys.argv) > 1 and sys.argv[1] == 'jackal':
    robot_module = 'jackal_obj'

# Import the specified robot module as robot_obj
robot_obj = __import__(robot_module)



## Configuration parameters
attempt_ID = '00'


iteration_quantity = 20
robot_morphology = 3
gpt_model = "gpt-4o"                    # gpt-3.5-turbo     | Use this for dev/testing
                                        # gpt-4 / gpt-4o    | Use this when deployed, more expensive
                                        # gpt-4o-mini       | Lightweight, less expensive than gpt4o
temperature_coefficient = 1.0           # Moderately stochastic @ 0.6 to 1.0
frequency_penalty_coefficient = 1.0     # Lightly penalize repetition @ 0.2
top_p_coefficient=1.0                   # Nucleus sampling for controlled randomness @ 0.85 to 0.6
omission_probability = 0.5
deployment_context = f"Consider a scenario where you are collaborating with a {robot_obj.form_factor} robot to locate and pick strawberries in a strawberry patch."



def main():
    pass





if __name__ == "__main__":
    main()
