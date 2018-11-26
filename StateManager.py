from StateLoader import StateLoader


class StateManager:

    def __init__(self):
        self.__state_loader = StateLoader()

        self.__questions = self.__state_loader.load_questions("path")
        self.__answers = self.__state_loader.load_answers("path")
        self.__current_state = self.__state_loader.load_states("path")
        self.__qtable = self.__state_loader.load_qtable("path")

    def get_current_state(self):
        return self.__current_state;

    def process_input(self):
        pass

    def choose_question(self):
        pass
