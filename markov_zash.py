import numpy as np
import random as rm
import itertools

NUMBER_OF_DEVICES = 29

def build_statespace():
    # since each device state is 0 or 1, the total number of states is 2^number_of_devices
    number_of_states = 2 ** NUMBER_OF_DEVICES
    states = [list(i) for i in itertools.product([0, 1], repeat=number_of_states)]
    return states

# def build_transition():



# The statespace
states = build_statespace()
print(len(states))