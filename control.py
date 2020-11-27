# control.py is the main control center for the led program, viewed as a state machine
import var
import util
import map
import time


class Controller(object):

    def __init__(self):
        self.state = 0
        self.map = map.Map()
        self.pause = False

    def tick(self):
        while not self.pause:
            self.map.tick()
            textMap = self.map.textMap()
            print(textMap)
            time.sleep(1)
            
    def pause(self):
        self.pause = True

    def restart(self):
        self.pause = False
        self.tick()

# c = Controller()
# c.tick()