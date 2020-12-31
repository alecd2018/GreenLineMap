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
        self.leds = ledControl.LEDControl()
        self.isPaused = False
        self.partying = False

    def tick(self):
        while not self.partying:
            if not self.isPaused:

                trains, stops = self.map.tick()
                self.leds.tick(trains, stops)

                textMap = self.map.textMap()

                # For Debugging:
                # print(textMap)

            time.sleep(1)

        while self.partying:
            if not self.isPaused:
                self.leds.party()
            else:
                time.sleep(1)
            
    def pause(self):
        print("Pausing")
        self.isPaused = True
        self.leds.pause()

    def restart(self):
        print("Restarting")
        self.isPaused = False

    def party(self):
        print("Partying")
        self.partying = True

    def trains(self):
        print("Running trains")
        self.partying = False