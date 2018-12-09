from StateManager import StateManager

finish = False

while not finish:
    state_manager = StateManager()

    response = None
    while not state_manager.finished():
        if response != -1:
            question = state_manager.choose_question()
        print(question)

        user_input = input('Enter your input:')

        response = state_manager.process_input(user_input)

    user_input = input('Press enter to make a new order or insert 1 to finish:')
    if user_input == "1":
        finish = True
    print("----------------------------")
