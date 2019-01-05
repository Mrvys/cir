from StateManager import StateManager
from listen import Listen
import time
from speech import Speech
from audio import Audio
import pygame as pg
import os

finish = False

state_manager = StateManager("man", "student")
listen = Listen()
speech = Speech()
audio = Audio()

while not finish:
    state_manager.restart()

    response = None
    while not state_manager.finished():
        if response != -1:
            question = state_manager.choose_question()
        print(question)
        audio.audio(question)

        #user_input = input('Enter your input:')

        user_input = listen.listen()
        #user_input = speech.detect()
        print(user_input)
        state_manager.process_input(user_input)

    user_input = input('Press enter to make a new order or insert 1 to finish:')
    if user_input == "1":
        finish = True
    print("----------------------------")