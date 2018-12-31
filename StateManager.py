from StateLoader import StateLoader
from TextRecognizer import TextRecognizer

import random


class StateManager:

    __question_prefix = "Would you like "
    __epsilon = 0.10  # TODO How and when should we decrease it?
    __learning_rate = 0.4  # TODO Fit the best
    __orders = {}
    __last_order = ""
    __last_questions = []
    gamma = 0.95  # discount rate

    def __init__(self, gender, group):
        self.__MAX_REWARD = 10
        self.__gender = gender
        self.__group = group
        try:
            self.__state_loader = StateLoader("../universalUserActions.json")
        except:
            self.__state_loader = StateLoader("./universalUserActions.json")

        try:
            self.__states = self.__state_loader.load_states("../states.json")
        except:
            self.__states = self.__state_loader.load_states("./states.json")
        self.__current_state_id = "A"
        self.__previous_state_id = "A"
        self.__qtable = self.__state_loader.load_qtable(gender, group, self.__states)
        self.__orders = self.__state_loader.load_orders(gender, group)

        self.__text_recognizer = TextRecognizer()

        if not self.still_learning():
            self.__learning_rate = 0.8

    def get_current_state(self):
        return self.__states[self.__current_state_id]

    def process_input(self, user_input):
        actions_available = list(self.get_current_state().get_transitions().keys())
        chosen_action = self.__text_recognizer.choose_most_sufficient(user_input, actions_available)

        if chosen_action in actions_available:
            self.update_qtable(chosen_action)

            if chosen_action == 'no':
                temp = self.__current_state_id
                self.__current_state_id = self.__previous_state_id
                self.__previous_state_id = temp
            else:
                self.__previous_state_id = self.__current_state_id
                self.__current_state_id = self.get_current_state().get_next_state(chosen_action)
        else:
            return -1

    def choose_question(self):
        rand = random.uniform(0, 1)

        if rand > self.__epsilon:  # exploitation
            chosen_action = self.get_max_q_action()
        else:  # exploration
            chosen_action = self.get_random_action()

        self.update_qtable(chosen_action)

        self.__previous_state_id = self.__current_state_id
        self.__current_state_id = self.get_current_state().get_next_state(chosen_action)

        self.__last_questions.append(chosen_action)
        if len(self.__last_questions) > 3:
            self.__last_questions = self.__last_questions[1:]

        return chosen_action + '?'

    def get_random_action(self):
        actions_available = list(self.get_current_state().get_transitions().keys())
        random_action = random.randint(0, len(actions_available) - 1)
        action_chosen = actions_available[random_action]

        if action_chosen in self.__last_questions:
            return self.get_random_action()

        return action_chosen

    def save_qtable(self):
        self.__state_loader.save_qtable(self.__qtable, self.__gender, self.__group)

    def save_orders(self):
        self.__state_loader.save_orders(self.__orders, self.__gender, self.__group)

    def finished(self):
        if self.get_current_state().is_final():
            self.__last_order = self.get_current_state().get_name()

            if self.__last_order in self.__orders:
                self.__orders[self.__last_order] += 1
            else:
                self.__orders[self.__last_order] = 1

            if self.still_learning():
                self.save_orders()
                self.save_qtable()

            drink_name = self.get_current_state().get_name()
            drink_price = self.get_current_state().get_price()
            print(f"OK, one {drink_name}, it's {drink_price} euro.")

            return True

        return False

    def update_qtable(self, action_chosen):
        if self.get_current_state().is_action_unexpected(action_chosen):
            for state_id, state in self.__states.items():
                if not state.requires_user():
                    for action in state.get_transitions():
                        if not state.is_action_unexpected(action) and self.__question_prefix + action_chosen == action:
                            self.update_qtable_cell("yes", state.get_next_state(action))
                            if not self.still_learning():
                                self.update_qtable_cell(action, state_id)

        else:
            self.update_qtable_cell(action_chosen, self.__current_state_id)

    def update_qtable_cell(self, action_chosen, state_id):
        current_q = self.__qtable[state_id][action_chosen]
        next_state_id = self.__states[state_id].get_next_state(action_chosen)
        reward = self.calculate_reward(action_chosen, next_state_id, state_id)
        delta_q = self.__learning_rate * (reward + self.gamma * self.get_max_q_value(next_state_id) - current_q)

        self.__qtable[state_id][action_chosen] = current_q + delta_q

    def get_max_q_action(self):
        max_value = 0
        max_actions = []
        first = True

        for action, value in self.__qtable[self.__current_state_id].items():
            # value += self.get_bias(action, value)

            if action in self.__last_questions:
                continue
            if first:
                first = False
                max_value = value
                max_actions = [action]
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions.append(action)

        if len(max_actions) > 1:
            random_max = random.randint(0, len(max_actions) - 1)
            max_actions = [max_actions[random_max]]

        return max_actions[0]

    def calculate_reward(self, action_chosen, next_state_id, state_id):
        reward = self.__states[state_id].get_reward(action_chosen)
        next_state = self.__states[next_state_id]

        if next_state.is_final() and next_state.get_name() in self.__orders:
            total = sum(self.__orders.values())
            bias = (self.__MAX_REWARD - next_state.get_price()) * self.__orders[next_state.get_name()] / total
            reward += bias

        return reward

    def get_max_q_value(self, state_id):
        q_values = self.__qtable[state_id].values()

        if len(q_values) == 0:
            return 0
        return max(q_values)

    def restart(self):
        self.__current_state_id = "A"
        self.__previous_state_id = "A"
        self.__last_questions = []

    def get_bias(self, action, value):
        bias = 0

        if action == self.__question_prefix + self.__last_order:
            bias += abs(value) * 0.5

        return bias

    def still_learning(self):
        return self.__epsilon > 0.01

