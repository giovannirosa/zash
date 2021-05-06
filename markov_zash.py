import numpy as np
import random as rm
import itertools
import csv

NUMBER_OF_DEVICES = 29
state_space = []
transition_space = []
transition_occurrences = []

# def build_statespace():
#     # since each device state is 0 or 1, the total number of states is 2^number_of_devices
#     number_of_states = 2 ** NUMBER_OF_DEVICES
#     states = [list(i) for i in itertools.product([0, 1], repeat=number_of_states)]
#     return states


def build_transition(row, last_state):
    current_state = row[0:29]
    if not current_state in state_space:
        state_space.append(current_state)
    if last_state is not None:
        transition = [last_state,current_state]
        if transition not in transition_space:
            print(row[30])
            transition_space.append(transition)
            transition_occurrences.append(1)
        transition_index = transition_space.index(transition)
        transition_occurrences[transition_index] += 1
        
        



with open('d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    last_state = None
    for row in spamreader:
        build_transition(row, last_state)
        last_state = row[0:29]

print(len(state_space))
# print(state_space)
print('')
print(len(transition_space))
# print(transition_space)
print('')
print(len(transition_occurrences))
# print(transition_occurrences)

transition_matrix = []
for state in state_space:
    print(state)
    matches = [transition for transition in transition_space if transition[0] == state]
    # print(matches)
    # print()
    total_occ = 0
    for match in matches:
        transition_index = transition_space.index(match)
        total_occ += transition_occurrences[transition_index]
        transition_state = {"state": match[0], "next_state": match[1], "value": transition_occurrences[transition_index]}
        # print(transition_state)
        transition_matrix.append(transition_state)
    for transition_state in transition_matrix:
        transition_state["value"] = transition_state["value"] / total_occ
        print(transition_state)
    print()

    
    