class State:

    def __init__(self, name, transitions, is_final, price, requires_user):
        self.__name = name
        self.__requires_user = requires_user  # if  user answer is required or assistant question
        self.__transitions = transitions  # map - key: transition word(action), value:(probability, next state, reward)
        # self.actions = actions  # list of possible questions from this state or customer answers
        # self.q_table = q_table  # map - key: transition word (like a sentence), value: q value
        # self.reward_table = reward_table  # map - key: transition word (like a sentence), value: reward value
        self.__is_final = is_final
        self.__price = price

    def get_next_state(self, action):
        return self.__transitions[action][1]

