import random
from openai import OpenAI

client = OpenAI()

def maybe_include(omission_prob, param_string):
    """Randomly omit a parameter string based on probability"""
    return param_string if random.random() > omission_prob else ""


def gpt4_prompt_reply(prompt: str) -> str:
    """Get a response from GPT-4"""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content



def build_prompt(parameter_values, states, deployment_context, omission_probability, gpt_assistant_prompt):
    """Build a prompt for GPT based on robot parameters and states"""
    
    # Shuffle states to avoid bias
    state_list = states[:-1]  # All states except the last one
    random.shuffle(state_list)
    unsure_state = states[-1]  # The "Unsure" state
    

    






    # Generate parameter strings based on the robot's current values
    param_strings = []
    for param_name, value in parameter_values.items():
        # Add parameter string generation logic here based on the value
        # This would need to be customized based on your parameter descriptions
        pass
        
    # Build expression string from parameter strings
    expression_string = " ".join([s for s in param_strings if s])
    
    # Get summarized expression using GPT
    summary_prompt = f"{deployment_context} Summarize the explanation below, focusing on describing the robot's actions in this scenario:\n{expression_string}"
    summarized_expression = gpt4_prompt_reply(summary_prompt)
    
    # Build the final prompt
    prompt = f"""
{gpt_assistant_prompt}

{deployment_context}

In this scenario, the robot can be in one of 5 possible states. The data in this list is in the format: "State Number: [State Name, State Description]"

{state_list[0]}

{state_list[1]}

{state_list[2]}

{state_list[3]}

{state_list[4]}

{unsure_state}

—————————

Below is a description of the robot using its body pose to express its internal state:

{summarized_expression}

—————————

Your task:

Please estimate what state you think the robot is in based on this description. If none of the states seem to match the description, select 'Unsure'.

Your response must be a single line in the exact format shown below (see example and reference):

[State_Number, State_Name]

Reference: 
State_Number = number of the selected robot state (e.g. S01)
State_Name = name of the selected robot state (e.g. Analyzing Object)
"""
    
    return prompt
