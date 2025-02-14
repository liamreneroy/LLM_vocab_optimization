# Imports
import sys
import numpy as np
import random
import time
random.seed(time.time())

from itertools import product

from openai import OpenAI
client = OpenAI()

from helper_functions import llm_prompt_reply
from prompt_builder import build_prompt


# Default to go1_obj
robot_module = 'go1_obj'

# Only change to jackal if explicitly specified
if len(sys.argv) > 1 and sys.argv[1] == 'jackal':
    robot_module = 'jackal_obj'

# Import the specified robot module as robot_obj
robot_obj = __import__(robot_module)

## Configuration parameters
attempt_ID = '00'

iteration_quantity = 100
llm_model = "gpt-4o"                    # gpt-3.5-turbo     | Use this for dev/testing
                                        # gpt-4 / gpt-4o    | Use this when deployed, more expensive
                                        # gpt-4o-mini       | Lightweight, less expensive than gpt4o
temperature_coefficient = 1.0           # Moderately stochastic @ 0.6 to 1.0
frequency_penalty_coefficient = 1.0     # Lightly penalize repetition @ 0.2
top_p_coefficient=1.0                   # Nucleus sampling for controlled randomness @ 0.85 to 0.6
omission_probability = 0.5

# The data in this should be in the format: "State Number: [State Name, State Description]"

# Used for Go1 robot
if robot_module == 'go1_obj':
    set_of_states = [  # 
        "S01: [Waiting for Input, The robot is in standby mode waiting for a command from the user]",
        "S02: [Analyzing Object, The robot is analyzing a target object in front of it on the ground]", 
        "S03: [Found Object, The robot has found a target object in front of it on the ground]",
        "S04: [Needs Help, The robot is experiencing an error and needs help from the user]",
        "S05: [Confused, The robot is confused and unsure what to do]",
        "S06: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
    ]

# Used for Jackal robot
elif robot_module == 'jackal_obj':
    set_of_states = [
        "S01: [Progressing, The robot is actively working on a task and does not require assistance]",
        "S02: [Alert, The robot is alerting that atttempting to get the user's attention]",
        "S03: [Accomplished, The robot has completed its task and reached its goal]",
        "S04: [Unsure, It is unclear as the robot does not appear to be in any of the described states.]"
    ]
# set_of_states = [
#     "S01: [Progressing, The robot is actively navigating toward the destination without needing user input.]",
#     "S02: [Alert, The robot is signaling for the user's attention, possibly requiring guidance or confirming directions.]",
#     "S03: [Accomplished, The robot has successfully reached the requested destination.]",
#     "S04: [Unsure, The robot is uncertain about its next action or location and may need user assistance.]"
# ]


llm_assistant_prompt = "You are an expert roboticist and understand how to design communicative expressions for human-robot interaction."

robot_instance = robot_obj.Robot(set_of_states)

deployment_context = f"Consider a scenario where you are collaborating with a {robot_instance.form_factor} robot to locate and pick strawberries in a strawberry patch."



printer = True # True or None



def main():
    # pass

    # Initialize error and total counters
    error_counter = 0
    total_counter = 0

    # Create robot object
    robot_instance = robot_obj.Robot(set_of_states)

    # Get action space shape, and use it to create a for loop that itterates all indices
    action_space_shape = robot_instance.get_action_space_shape()

    # Itterate through all possible actions in action space
    # count = 0
    # for indices in product(*(range(dim) for dim in action_space_shape)):
    #     count += 1
    #     print(f"Action {count}:")
    #     robot_instance.set_active_parameter(list(indices))
    #     print(robot_instance.active_parameters)
    #     print(robot_instance.generate_description(omission_probability))
    #     print("\n\n")

    # Set active parameters based on action space shape for robot_instance
    test_value_A = [0, 0, 1, 0, 1, 0]  # Example values within range for each parameter
    test_value_B = [1, 2, 0, 2, 0, 1]  # Example values within range for each parameter
    test_value_C = [0, 1, 2, 1, 1, 2]  # Example values within range for each parameter
    set_set = [test_value_A, test_value_B, test_value_C]

    for test_values in set_set:
        robot_instance.set_active_parameter(test_values)

        # Five iterations for loop
        for iteration in range(iteration_quantity):

            if printer:
                print(f"**********************************************************************")
                print(f"ITERATION {iteration+1} FOR {robot_instance.active_parameters}")
                print(f"**********************************************************************")

            # Generate description with test values and omission probability
            raw_description = robot_instance.generate_description(omission_probability)

            # Prepare a promt with context + robot description
            summary_prompt = f"{deployment_context} Summarize the explanation below, focusing on describing the robot's actions in this scenario:\n{raw_description}"
            
            ### SWAP UNCOMMENT TO DISABLE TEST AND ENABLE LLM
            # Summarize the context + robot description using llm 
            summarized_expression = raw_description
            # summarized_expression = llm_prompt_reply(prompt=summary_prompt, 
            #                                           client=client, 
            #                                           llm_model=llm_model, 
            #                                           llm_assistant_prompt=llm_assistant_prompt, 
            #                                           temperature_coefficient=temperature_coefficient, 
            #                                           frequency_penalty_coefficient=frequency_penalty_coefficient, 
            #                                           top_p_coefficient=top_p_coefficient)


            # Print before and after summary
            if printer:
                print(f"\nRAW DESCRIPTION:\n{raw_description}")
                print(f"\nLLM SUMMARY:\n{summarized_expression}")

            # Pass summarized expression to prompt builder, along with set of states and robot_instance parameters 
            acc_proxy_prompt = build_prompt(expression_string=summarized_expression, state_list=set_of_states, deployment_context=deployment_context, llm_assistant_prompt=llm_assistant_prompt)
            
            if printer:
                print(f"\n\nACCURACY PROXY PROMPT:\n~~~{acc_proxy_prompt}~~~\n\n")


            ### SWAP UNCOMMENT TO DISABLE TEST AND ENABLE LLM
            options = ["[S01, Waiting for Input]", "[S02, Analyzing Object]", "[S03, Found Object]", "[S04, Needs Help]", "[S05, Confused]", "[S06, Unsure]"]
            acc_proxy_reply = random.choice(options)
            # Run the prompt through the accuracy proxy model
            # acc_proxy_reply = llm_prompt_reply(acc_proxy_prompt, client, llm_model, llm_assistant_prompt, temperature_coefficient, frequency_penalty_coefficient, top_p_coefficient)

            # Parse the accuracy proxy reply to identify the state
            state_code, _ = acc_proxy_reply.strip("[]").split(", ")
            state_code = state_code.strip("'")
            
            # Check if the state code exists within the dictionary
            if state_code in robot_instance.action_space[tuple(test_values)]:
                # Increment the count for the identified state in the action space
                robot_instance.action_space[tuple(test_values)][state_code] += 1
                total_counter += 1

                if printer:
                    # Output the identified state code
                    print(f"Identified state code: {state_code}")
                    # Output the updated action space
                    print(f"Updated action space: {robot_instance.action_space[tuple(test_values)]}\n")

            else:
                # Output an error message if the state code does not exist
                error_counter += 1
                total_counter += 1
                
                if printer:
                    print(f"Error: State code '{state_code}' does not exist in the action space.\n")

            #     # Log the reply from the accuracy proxy model to the robot_instance action_space
            #     robot_instance.action_space[1, 1, 0, 0, 1, 0] = acc_proxy_reply
        
        if printer:
            print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(f"COMPLETED ALL {iteration_quantity} ITERATIONS FOR {robot_instance.active_parameters}")
            print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n")

    if printer:
        print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"COMPLETED ALL COMBINATIONS")
        print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")


    # Save the numpy array robot_instance.action_space to a file 
    save_string = robot_module + "_acc_array_" + attempt_ID + ".npy"
    np.save(f"./../data/acc_arrays/{save_string}", robot_instance.action_space)

    # # Calculate the distance term for each action in action space based on the selected distance approach
    # # distance_terms = calculate_distance_terms(robot_instance.action_space)

    # # Analyze the action space for the robot_instance using cost function and determine the best action
    # # best_action = analyze_action_space(robot_instance.action_space)

    # # Log the best action to an external spreadsheet
    # #log_data(.......)

    # # Return the best action in terminal
    # #print(f"\n\nBest action: {best_action}")


if __name__ == "__main__":
    main()
