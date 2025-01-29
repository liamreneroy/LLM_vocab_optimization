# Imports
import sys
import numpy as np
import random
import time
random.seed(time.time())

from openai import OpenAI
client = OpenAI()

from helper_functions import maybe_include, gpt4_prompt_reply
from prompt_builder import build_prompt


# Default to go1_obj
robot_module = 'go1_obj'

# Only change to jackal if explicitly specified
if len(sys.argv) > 1 and sys.argv[1] == 'jackal':
    robot_module = 'jackal_obj'

# Import the specified robot module as robot_obj
robot_obj = __import__(robot_module)
robot_instance = robot_obj.Robot()

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
deployment_context = f"Consider a scenario where you are collaborating with a {robot_instance.form_factor} robot to locate and pick strawberries in a strawberry patch."

set_of_states = [
    "S01: [Waiting for Input, The robot is in standby mode waiting for a command from the user]",
    "S02: [Analyzing Object, The robot is analyzing a target object in front of it on the ground]", 
    "S03: [Found Object, The robot has found a target object in front of it on the ground]",
    "S04: [Needs Help, The robot is experiencing an error and needs help from the user]",
    "S05: [Confused, The robot is confused and unsure what to do]",
    "S06: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
]

gpt_assistant_prompt = "You are an expert roboticist and understand how to design communicative expressions for human-robot interaction."


###  Test helper functions 
# test_values = [1, 1, 0, 0, 1, 0]
# test_prompt = "Write me a 3 sentence story about a robot in Paris."
# test_reply = gpt4_prompt_reply(test_prompt, client, gpt_model, gpt_assistant_prompt, temperature_coefficient, frequency_penalty_coefficient, top_p_coefficient)
# print(f"\nTest reply: {test_reply}")




def main():
    pass

    # build_prompt(parameter_values=test_values, states=set_of_states, deployment_context=deployment_context, omission_probability=omission_probability, gpt_assistant_prompt=gpt_assistant_prompt)
    




if __name__ == "__main__":
    main()
