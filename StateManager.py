from StateLoader import StateLoader
from TextRecognizer import TextRecognizer

import random


class StateManager:

    __question_prefix = "Would you like "
    __epsilon = 0.0  # TODO How and when should we decrease it?
    __learning_rate = 0.9  # TODO Fit the best
    gamma = 0.95  # discount rate

    def __init__(self, gender, group):
        self.__gender = gender
        self.__group = group

        self.__state_loader = StateLoader("./universalUserActions.json")

        # self.__questions = self.__state_loader.load_questions("path")
        # self.__answers = self.__state_loader.load_answers("path")
        self.__states = self.__state_loader.load_states("./states.json")
        self.__current_state_id = "A"
        self.__previous_state_id = "A"
        self.__qtable = self.__state_loader.load_qtable(gender, group, self.__states)

        self.__last_order = ""
        self.__orders = {}
        self.__last_questions = []

        self.__text_recognizer = TextRecognizer()

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

    def finished(self):
        if self.get_current_state().is_final():
            self.__last_order = self.get_current_state().get_name()

            if self.__last_order in self.__orders:
                self.__orders[self.__last_order] += 1
            else:
                self.__orders[self.__last_order] = 1

            self.save_qtable()

            drink_name = self.get_current_state().get_name()
            drink_price = self.get_current_state().get_price()
            print(f"OK, one {drink_name}, it's {drink_price} euro.")

            return True

        return False

    def get_most_popular_order_actions(self):
        max_value = 0
        max_orders = []
        first = True
        for order, value in self.__orders.items():
            if first:
                first = False
                max_value = value
                max_orders = [self.__question_prefix + order]
            elif value > max_value:
                max_orders = [self.__question_prefix + order]
                max_value = value
            elif value == max_value:
                max_orders.append(self.__question_prefix + order)

        return max_orders

    def update_qtable(self, action_chosen):
        current_q = self.__qtable[self.__current_state_id][action_chosen]
        reward = self.get_current_state().get_reward(action_chosen)
        next_state_id = self.get_current_state().get_next_state(action_chosen)
        delta_q = self.__learning_rate * (reward + self.gamma * self.get_max_q_value(next_state_id) - current_q)

        self.__qtable[self.__current_state_id][action_chosen] = current_q + delta_q

    def get_max_q_action(self):
        max_value = 0
        max_actions = []
        first = True

        for action, value in self.__qtable[self.__current_state_id].items():
            value += self.get_bias(action, value)

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

        if action in self.get_most_popular_order_actions():
            bias += abs(value) * 0.5

        return bias
