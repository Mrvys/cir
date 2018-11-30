class State:

    def __init__(self, name, is_final, price, requires_user, transitions):
        self.__name = name
        self.__requires_user = requires_user  # if  user answer is required or assistant question

        # map - key: transition word(action), value:(probability, next state, reward)
        self.__transitions = transitions

        # self.q_table = q_table  # map - key: transition word (like a sentence), value: q value
        self.__is_final = is_final
        self.__price = price

    def get_next_state(self, action):
        return self.__transitions[action][1]

    def get_max_q(self):
        pass
