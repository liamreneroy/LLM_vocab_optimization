# Imports
import sys
import numpy as np
import random
import time
random.seed(time.time())

from openai import OpenAI
client = OpenAI()


from prompt_builder import build_prompt, gpt4_prompt_reply


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

set_of_states = [
    "S01: [Waiting for Input, The robot is in standby mode waiting for a command from the user]",
    "S02: [Analyzing Object, The robot is analyzing a target object in front of it on the ground]", 
    "S03: [Found Object, The robot has found a target object in front of it on the ground]",
    "S04: [Needs Help, The robot is experiencing an error and needs help from the user]",
    "S05: [Confused, The robot is confused and unsure what to do]",
    "S06: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
]

gpt_assistant_prompt = "You are an expert roboticist and understand how to design communicative expressions for human-robot interaction."

# Helper Functions

# Simple pass-return which passes a string to GPT4o model and returns the reply
def gpt4_prompt_reply(prompt: str) -> str:
            
    # calling GPT client
    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": gpt_assistant_prompt},  # System message with custom prompt
            {"role": "user", "content": prompt}],                 # User input
        temperature=temperature_coefficient,
        frequency_penalty=frequency_penalty_coefficient,
        top_p=top_p_coefficient
    )

    # Return the assistant's reply
    return completion.choices[0].message.content




def main():
    

    build_prompt(parameter_values, states=set_of_states, deployment_context=deployment_context, omission_probability=omission_probability, gpt_assistant_prompt=gpt_assistant_prompt)
    




if __name__ == "__main__":
    main()
