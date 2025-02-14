import random
import sys

def build_prompt(expression_string, state_list, deployment_context, llm_assistant_prompt):
    """Build a prompt for llm based on robot parameters and states"""

    # Shuffle all states except the last one
    shuffled_states = state_list[:-1]
    random.shuffle(shuffled_states)
    shuffled_states.append(state_list[-1])  # Ensure the last state is always last
    shuffled_states_str = "\n".join(shuffled_states)

    prompt = f'''
{llm_assistant_prompt}

{deployment_context}

In this scenario, the robot can be in one of {len(state_list)} possible states. The data in this list is in the format: "State Number: [State Name, State Description]"

{shuffled_states_str}

—————————

Below is a description of the robot using its body pose to express its internal state:

{expression_string}

—————————
    
Your task:

Please estimate what state you think the robot is in based on this description. If none of the states seem to match the description, select 'Unsure'.

Your response must be a single line in the exact format shown below (see example and reference):

[State_Number, State_Name]

Reference: 
State_Number = number of the selected robot state (e.g. S01)
State_Name = name of the selected robot state (e.g. Analyzing Object)
'''
    
    return prompt

# Test the build_prompt function
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "test":
    summarized_expression = "The robot is analyzing a target object in front of it on the ground while leaning forward slightly with its head tilted down."

    set_of_states = [
        "S01: [Waiting for Input, The robot is in standby mode waiting for a command from the user]",
        "S02: [Analyzing Object, The robot is analyzing a target object in front of it on the ground]", 
        "S03: [Found Object, The robot has found a target object in front of it on the ground]",
        "S04: [Needs Help, The robot is experiencing an error and needs help from the user]",
        "S05: [Confused, The robot is confused and unsure what to do]",
        "S06: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
    ]    
    
    deployment_context = f"Consider a scenario where you are collaborating with a dog-shaped robot to locate and pick strawberries in a strawberry patch."
    
    llm_assistant_prompt = "You are an expert roboticist and understand how to design communicative expressions for human-robot interaction."

    acc_proxy_prompt = build_prompt(expression_string=summarized_expression, state_list=set_of_states, deployment_context=deployment_context, llm_assistant_prompt=llm_assistant_prompt)
    
    print(acc_proxy_prompt)

