import random


def maybe_include(omission_prob, param_string):
    """Randomly omit a parameter string based on probability"""
    return param_string if random.random() > omission_prob else ""