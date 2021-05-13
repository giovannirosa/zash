# import csv

# NUMBER_OF_DEVICES = 29


class MarkovChain:
    def __init__(self):
        self.state_space = []
        self.transition_space = []
        self.transition_matrix = []

    def build_transition(self, current_state, last_state):
        if not current_state in self.state_space:
            self.state_space.append(current_state)
        if last_state is not None:
            transition_col = next(
                (transition_col for transition_col in self.transition_matrix if last_state == transition_col["state"]), None)
            if transition_col is None:
                transition_col = {"state": last_state,
                                  "next_states": [], "total_occ": 1}
                self.transition_matrix.append(transition_col)
            else:
                transition_col["total_occ"] += 1

            next_state = next(
                (next_state for next_state in transition_col["next_states"] if current_state == next_state["state"]), None)
            if next_state is None:
                transition_col["next_states"].append(
                    {"state": current_state, "occurrences": 1, "percentage": 1 / transition_col["total_occ"]})
            else:
                next_state["occurrences"] += 1

            for next_state_it in transition_col["next_states"]:
                next_state_it["percentage"] = next_state_it["occurrences"] / \
                    transition_col["total_occ"]

            transition = [last_state, current_state]
            if transition not in self.transition_space:
                self.transition_space.append(transition)

    def get_probability(self, current_state, last_state):
        if [last_state, current_state] not in self.transition_space:
            return 0
        prob = 0
        transition_col = next(
            (transition_col for transition_col in self.transition_matrix if last_state == transition_col["state"]), None)
        if transition_col is not None:
            next_state = next(
                (next_state for next_state in transition_col["next_states"] if current_state == next_state["state"]), None)
            if next_state is not None:
                prob = next_state["percentage"]
        return prob


# markov_chain = MarkovChain()

# with open('d6_2m_0tm.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',')
#     next(spamreader)
#     last_state = None
#     for row in spamreader:
#         current_state = list(map(int, row[0:NUMBER_OF_DEVICES]))
#         markov_chain.build_transition(current_state, last_state)
#         last_state = current_state


# print(len(markov_chain.state_space))
# print(len(markov_chain.transition_matrix))
# print(len(markov_chain.transition_space))
# print(markov_chain.transition_matrix)
