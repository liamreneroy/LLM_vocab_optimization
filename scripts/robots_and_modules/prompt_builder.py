import random
import sys

def build_prompt(expression_string, state_list, deployment_context, llm_assistant_prompt, expression_modality):
    """Build a prompt for llm based on robot parameters and states"""

    # Shuffle all states except the last one
    shuffled_states = state_list[:-1]
    random.shuffle(shuffled_states)
    shuffled_states.append(state_list[-1])  # Ensure the last state is always last
    shuffled_states_str = "\n".join(shuffled_states)

    prompt = f'''
{llm_assistant_prompt}

{deployment_context}

In this scenario, the robot can be in one of {len(state_list)-1} possible states. The data in this list is in the format: "State Number: [State Name, State Description]"

{shuffled_states_str}

—————————

Below is a description of the robot using {expression_modality} to express its state:

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
            "S01: [Processing, The robot is calculating its navigation route to the delivery destination.]",
            "S02: [Navigating, The robot is navigating normally towards the delivery destination.]",
            "S03: [Danger, The robot is signaling for the user's attention due to a dangerous hazard.]",
            "S04: [Stuck, The robot is signaling for the user's attention as its wheel being stuck.]",
            "S05: [Accomplished, The robot is signaling that it has successfully reached the delivery destination.]",
            "S06: [Unsure, The robot's state is unclear as it does not appear to be in any of the described states.]"
        ]
    
    deployment_context = f"Consider a scenario where you are collaborating with a rover-shaped robot to navigate through a warehouse and deliver packages to different locations."

    llm_assistant_prompt = "You are an expert roboticist and understand how to design communicative expressions for human-robot interaction."

    robot_modality = "audio beeps"

    acc_proxy_prompt = build_prompt(expression_string=summarized_expression, 
                                    state_list=set_of_states, 
                                    deployment_context=deployment_context, 
                                    llm_assistant_prompt=llm_assistant_prompt,
                                    expression_modality=robot_modality)
    
    print(acc_proxy_prompt)

