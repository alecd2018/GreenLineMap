# control.py is the main control center for the led program, viewed as a state machine
import vars
import util


class Controller(object):

    def __init__(self):
        self.state = 0

    def tick(self):
        return

    def pause(self):
        return