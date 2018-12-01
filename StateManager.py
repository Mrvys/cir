from StateLoader import StateLoader


class StateManager:

    def __init__(self):
        self.__state_loader = StateLoader("./universalUserActions.json")

        # self.__questions = self.__state_loader.load_questions("path")
        # self.__answers = self.__state_loader.load_answers("path")
        self.__states = self.__state_loader.load_states("./states.json")
        self.__current_state = self.__states["A"]
        self.__qtable = self.__state_loader.load_qtable("./qtable.json", self.__states)

    def get_current_state(self):
        return self.__current_state

    def process_input(self, user_input):
        pass

    def choose_question(self):
        pass

    def save_qtable(self):
        self.__state_loader.save_qtable("./qtable.json", self.__qtable)

    def finished(self):
        return not self.__current_state.is_final()

