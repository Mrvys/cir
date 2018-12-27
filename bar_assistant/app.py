import os
import sys
import time
from time import sleep
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
from threading import Timer

from StateManager import StateManager


class BarAssistantApp(object):

    def __init__(self, path='./bar_assistant/'):
        self.PATH = os.path.abspath(path) + '/'
        self.VALUE_ROLE = QtCore.Qt.UserRole
        self.STATUS_WAITING = 'Waiting'
        self.STATUS_PROCESSING_REQUEST = 'Processing request'
        self.AVATAR = {'normal': {'name':'smile.jpg'},
                       'talking': {'name':'smile_talking.gif'}}
        self.PICS_PATH = './pics/'
        self.UI_PATH = './ui/'
        self.CHAR_DELAY_IN_MILIS = 3
        self.MAGIC_CONSTANT = 1.75

        self.app = None
        self.assistant = None
        self.window = None
        self.status = None
        self.avatar = None
        self.chat = None  # type: Chat
        self.chatArea = None
        self.userInput = None

        self.state_manager = StateManager("man", "middle")
        self.last_question = None

        self.init()

    def init(self):
        try:
            self.app = QtWidgets.QApplication([])
            self.window = QtWidgets.QMainWindow()

            self.load_resources()

            with open(self.PATH + self.UI_PATH + 'bar_assistant.ui') as f:
                uic.loadUi(f, self.window)
            icon = QtGui.QIcon(self.PATH + self.PICS_PATH + self.AVATAR['normal']['name'])  # ikonu
            self.window.setWindowIcon(icon)

            self.init_chat()
            self.init_assistant()
            self.init_user_area()
            self.init_signals()

            self.choose_first_question()

        except Exception as e:
            self.show_error('Application could not initiate properly due to this error: \n' + str(e))
            sys.exit(1)

    def init_assistant(self):
        self.status = self.STATUS_WAITING

        self.assistant = Assistant()
        self.init_avatar_area()
        self.refresh_assistant()


    def init_avatar_area(self):
        # získáme oblast s posuvníky z Qt Designeru
        avatar_area = self.window.findChild(QtWidgets.QLabel, 'avatar')

        pixmap = self.AVATAR['normal']['pixmap']
        avatar_area.setPixmap(pixmap)

        # Optional, resize window to image size
        avatar_area.resize(pixmap.width(), pixmap.height())
        self.avatar = avatar_area

    def init_user_area(self):
        self.userInput = self.window.findChild(QtWidgets.QWidget, 'userInput')
        self.userInput.setFocus()

    def init_signals(self):
        action = self.window.findChild(QtWidgets.QWidget, 'sendButton')
        action.clicked.connect(lambda: self.receive_message())
        action = self.window.findChild(QtWidgets.QWidget, 'speakButton')
        action.clicked.connect(lambda: self.speak_capture())
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.window)
        shortcut.activated.connect(self.send_message)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self.window)
        shortcut.activated.connect(self.speak_capture)

    def load_resources(self):
        self.AVATAR['normal']['pixmap'] = QtGui.QPixmap(self.PATH + self.PICS_PATH + self.AVATAR['normal']['name'])
        self.AVATAR['talking']['movie'] = QtGui.QMovie(self.PATH + self.PICS_PATH + self.AVATAR['talking']['name'])

    def choose_first_question(self):
        self.last_question = self.state_manager.choose_question()
        self.send_message(self.last_question)

    def receive_message(self):
        self.set_enable_user_input(False)
        self.status = self.STATUS_PROCESSING_REQUEST
        self.refresh_assistant()
        self.app.processEvents()

        inputArea = self.window.findChild(QtWidgets.QLineEdit, 'userInput')
        message = inputArea.text()

        inputArea.setText('')
        self.chat.putMessage('User', message)
        self.refresh_chat()

        self.app.processEvents()

        response = self.state_manager.process_input(message)

        if self.state_manager.finished():
            drink_name = self.state_manager.get_current_state().get_name()
            drink_price = self.state_manager.get_current_state().get_price()
            self.send_message(f"OK, one {drink_name}, it's {drink_price} euro.")

            self.state_manager.restart()

        if response != -1:
            self.last_question = self.state_manager.choose_question()
        else:
            self.send_message("Sorry, I don't understand.")
        self.send_message(self.last_question)

    def send_message(self, message):
        self.status = self.STATUS_WAITING

        speak_length = len(message) * self.CHAR_DELAY_IN_MILIS / 100 * self.MAGIC_CONSTANT

        timer = Timer(speak_length, self.shut_up)
        timer.start()

        # self.refresh_assistant()
        # message = self.assistant.response()
        self.chat.putMessage('Assistant', '')
        for char in message:
            self.chat.putChar(char)
            self.refresh_chat()
            for _ in range(int(self.CHAR_DELAY_IN_MILIS)):
                sleep(0.01)
                self.app.processEvents()

        self.set_enable_user_input(True)

        self.userInput.setFocus()

    def shut_up(self):
        self.avatar.setPixmap(self.AVATAR['normal']['pixmap'])

    def speak_capture(self):
        message = 'Capturing speech.'
        self.chat.putMessage('Assistant', message)
        self.refresh_chat()

    def init_chat(self):
        self.chatArea = self.window.findChild(QtWidgets.QTextEdit, 'chat')
        self.chat = Chat()

    def refresh(self):
        self.refresh_chat()
        self.refresh_assistant()

    def refresh_assistant(self):
        lineedit = self.window.findChild(QtWidgets.QLineEdit, 'status')
        lineedit.setText(self.status)
        if self.status == self.STATUS_WAITING:
            self.avatar.setPixmap(self.AVATAR['normal']['pixmap'])
        if self.status == self.STATUS_PROCESSING_REQUEST:
            movie = self.AVATAR['talking']['movie']
            self.avatar.setMovie(movie)
            movie.start()

    def refresh_chat(self):
        self.chatArea.setText(self.chat.getText())

    def run(self):
        self.window.show()

        return self.app.exec()

    def show_error(self, msg):
        print(msg)
        QtWidgets.QMessageBox.critical(self.window, 'Error', msg)

    def set_enable_user_input(self, enable):
        sendButton = self.window.findChild(QtWidgets.QWidget,'sendButton')
        sendButton.setEnabled(enable)
        speakButton = self.window.findChild(QtWidgets.QWidget,'speakButton')
        speakButton.setEnabled(enable)
        lineedit = self.window.findChild(QtWidgets.QWidget,'userInput')
        lineedit.setEnabled(enable)


class AvatarWidget(QtWidgets.QWidget):

    def __init__(self, app):
        super().__init__()  # musíme zavolat konstruktor předka

        self.AVATAR = app.AVATAR['QtSvg']

    def paintEvent(self, event):
        rect = event.rect()  # získáme informace o překreslované oblasti

        painter = QtGui.QPainter(self)  # budeme kreslit

        rect = QtCore.QRectF(rect.left(), rect.top(), 100, 100)

        self.AVATAR.render(painter, rect)


class Chat:

    def __init__(self):
        self.chat = []

    def putMessage(self, username, text):
        message = {'user': username,
                   'text': text}
        self.chat.append(message)

    def getText(self):
        # text = '\n'.join([str(msg.username). + ': 'for msg in self.chat])
        text = ''
        for msg in self.chat:
            username = str(msg['user']).ljust(12,' ')
            message = username + ': ' + msg['text']
            text += message + '\n'
        return text

    def putChar(self, char):
        self.chat[-1]['text'] += char


class Assistant:

    def request(self, text):
        pass

    def response(self):
        return 'Tell me something.'


def main(path='../bar_assistant/'):
    app = BarAssistantApp(path)
    app.run()


if __name__ == '__main__':
    main()