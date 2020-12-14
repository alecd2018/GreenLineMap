# control.py is the main control center for the led program, viewed as a state machine
import var
import util
import map
import time
import ledControl


class Controller(object):

    def __init__(self):
        self.state = 0
        self.map = map.Map()
        self.leds = ledControl.ledControl()
        self.isPaused = False

    def tick(self):
        while True:
            if not self.isPaused:

                self.map.tick()
                self.leds.tick()

                textMap = self.map.textMap()
                print(textMap)

            time.sleep(1)
            
    def pause(self):
        print("Pausing")
        self.isPaused = True
        self.leds.pause()

    def restart(self):
        self.isPaused = False
        self.leds.resume()