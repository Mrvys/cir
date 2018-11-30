import json

from State import State


class StateLoader:

    def __init__(self, universal_user_actions_path):
        self.__universal_user_actions = self.__load_actions(universal_user_actions_path)

    def __load_actions(self, path):
        actions = {}

        with open(path) as file:
            data = json.load(file)

        for action in data:
            actions[action] = tuple(data[action])

        return actions

    def load_states(self, filename):
        with open(filename) as file:
            data = json.load(file)

        states = {}

        for state_id in data:
            transitions = {}

            if data[state_id]["transitions"]:
                for action in data[state_id]["transitions"]:
                    transitions[action] = tuple(data[state_id]["transitions"][action])
                    pass

            if data[state_id]["requires_user"]:
                transitions.update(self.__universal_user_actions)

            new_state = State(data[state_id]["name"], data[state_id]["final"], data[state_id]["price"],
                              data[state_id]["requires_user"], transitions)
            states[state_id] = new_state

        return states

    def load_qtable(self, filename, states):
        pass  # should return the qTable read from the file or crete new one

    def save_qtable(self, filename):
        pass  # should save updated q table to a file

    def load_questions(self, filename):
        pass

    def load_answers(self, filename):
        pass
