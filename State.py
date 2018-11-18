class State:

    def __init__(self, name, transitions, questions):
        self.name = name
        self.transitions = transitions # map - key: transition word (like a sentence), value: next state
        self.questions = questions # list of possible questions from this state

    def change_state(self, user_input):
        pass

    def choose_question(self):
        return self.questions[0]

