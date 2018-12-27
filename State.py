class State:

    def __init__(self, name, is_final, price, requires_user, transitions):
        self.__name = name
        self.__requires_user = requires_user  # if  user answer is required or assistant question

        # map - key: transition word(action), value:(probability, next state, reward, isUnexpected)
        self.__transitions = transitions

        # self.q_table = q_table  # map - key: transition word (like a sentence), value: q value
        self.__is_final = is_final
        self.__price = price

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_next_state(self, action):
        return self.__transitions[action][1]

    def get_transitions(self):
        return self.__transitions

    def is_final(self):
        return self.__is_final

    def get_reward(self, action):
        return self.__transitions[action][2]

    def is_action_unexpected(self, action):
        return self.__transitions[action][3]

    def requires_user(self):
        return self.__requires_user
