from StateManager import StateManager

state_manager = StateManager()

while state_manager.finished():
    question = state_manager.choose_question()
    print(question)

    user_input = input('Enter your input:')

    state_manager.process_input(user_input)
