import random
from openai import OpenAI
client = OpenAI()

def maybe_include(omission_prob, param_string):
    """Randomly omit a parameter string based on probability"""
    return param_string if random.random() > omission_prob else ""



# Simple pass-return which passes a string to GPT4o model and returns the reply
def gpt4_prompt_reply(prompt: str, client, gpt_model: str, gpt_assistant_prompt: str, 
                     temperature_coefficient: float = 1.0,
                     frequency_penalty_coefficient: float = 1.0,
                     top_p_coefficient: float = 1.0) -> str:
            
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
