from StateLoader import StateLoader
from TextRecognizer import TextRecognizer

import random


class StateManager:

    def __init__(self):
        self.__epsilon = 0.5  # TODO How and when should we decrease it?

        self.__state_loader = StateLoader("./universalUserActions.json")

        # self.__questions = self.__state_loader.load_questions("path")
        # self.__answers = self.__state_loader.load_answers("path")
        self.__states = self.__state_loader.load_states("./states.json")
        self.__current_state_id = "A"
        self.__qtable = self.__state_loader.load_qtable("./qtable.json", self.__states)

        self.__text_recognizer = TextRecognizer()

    def get_current_state(self):
        return self.__states[self.__current_state_id]

    def process_input(self, user_input):
        actions_available = list(self.get_current_state().get_transitions().keys())
        chosen_action = self.__text_recognizer.choose_most_sufficient(user_input, actions_available)

        self.update_qtable(chosen_action)

        self.__current_state_id = self.get_current_state().get_next_state(chosen_action)

    def choose_question(self):
        rand = random.uniform(0, 1)

        if rand > self.__epsilon:  # exploitation
            chosen_action = self.get_max_q_action()
        else:  # exploration
            actions_available = list(self.get_current_state().get_transitions().keys())
            random_action = random.randint(0, len(actions_available) - 1)
            chosen_action = actions_available[random_action]

        self.update_qtable(chosen_action)

        self.__current_state_id = self.get_current_state().get_next_state(chosen_action)

        return chosen_action + '?'

    def save_qtable(self):
        self.__state_loader.save_qtable("./qtable.json", self.__qtable)

    def finished(self):
        if self.get_current_state().is_final():
            self.save_qtable()

            drink_name = self.get_current_state().get_name()
            drink_price = self.get_current_state().get_price()
            print(f"OK, one {drink_name}, it's {drink_price} euro.")

            return True

        return False

    def update_qtable(self, action_chosen):
        pass

    def get_max_q_action(self):
        max_value = 0
        max_actions = []

        for action, value in self.__qtable[self.__current_state_id].items():
            if value > max_value:
                max_actions = [action]
            elif value == max_value:
                max_actions.append(action)

        if len(max_actions) > 1:
            random_max = random.randint(0, len(max_actions) - 1)
            max_actions = [max_actions[random_max]]

        return max_actions[0]
