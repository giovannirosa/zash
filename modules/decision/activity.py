class ActivityComponent:
    def __init__(self):
        self.markov_chain = MarkovChain()
        self.is_markov_building = True

    # check next state probability using a Markov Chain
    # updates transition matrix with successful requests
    def verify_activity(self, current_state, last_state):
        print("Activity Component")
        print("Verify activities")
        print("From: {}".format(last_state))
        print("To: {}".format(current_state))
        if self.is_markov_building:
            self.markov_chain.build_transition(current_state, last_state)
            return True
        else:
            prob = self.markov_chain.get_probability(current_state, last_state)
            if prob > 0:
                self.markov_chain.build_transition(current_state, last_state)
                print("Activity is valid!")
                return True
            else:
                print("Activity is NOT valid!")
                return False


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