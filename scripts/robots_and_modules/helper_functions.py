import random
import numpy as np
from typing import Optional


from openai import OpenAI
client = OpenAI()

# Define a function to create a fresh dictionary
def create_state_dict(set_of_states):
    return {state[:3]: 0 for state in set_of_states}


def maybe_include(omission_prob, param_string):
    """Randomly omit a parameter string based on probability"""
    return param_string if random.random() > omission_prob else ""


def llm_prompt_reply(
    prompt: str,
    client,
    llm_model: str,
    llm_assistant_prompt: str,
    max_output_tokens: int = 200,
    reasoning_effort: Optional[str] = "low",
) -> str:
    messages = [
        {"role": "system", "content": llm_assistant_prompt},
        {"role": "user", "content": prompt},
    ]

    kwargs = {
        "model": llm_model,
        "input": messages,
        "max_output_tokens": max_output_tokens,
    }
    if reasoning_effort is not None:
        kwargs["reasoning"] = {"effort": reasoning_effort}

    response = client.responses.create(**kwargs)

    # Preferred if your SDK exposes it
    text = getattr(response, "output_text", None)
    if text:
        return text

    # Robust fallback: scan output for the assistant message text
    for item in (response.output or []):
        if getattr(item, "type", None) == "message":
            for c in (item.content or []):
                if getattr(c, "type", None) in ("output_text", "text"):
                    return c.text

    raise RuntimeError(f"No assistant text found. Raw response: {response}")




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# OLD CALL WITH PRE-REASONING CHATGPT4o MODEL - KEEP FOR REFERENCE
# # Simple pass-return which passes a string to GPT4o model and returns the reply
# def llm_prompt_reply(prompt: str, client, llm_model: str, llm_assistant_prompt: str, 
#                      temperature_coefficient: float = 1.0,
#                      frequency_penalty_coefficient: float = 1.0,
#                      top_p_coefficient: float = 1.0) -> str:
            
#     # calling llm client
#     completion = client.chat.completions.create(
#         model=llm_model,
#         messages=[
#             {"role": "system", "content": llm_assistant_prompt},  # System message with custom prompt
#             {"role": "user", "content": prompt}],                 # User input
#         temperature=temperature_coefficient,
#         frequency_penalty=frequency_penalty_coefficient,
#         top_p=top_p_coefficient
#     )

#     # Return the assistant's reply
#     return completion.choices[0].message.content

