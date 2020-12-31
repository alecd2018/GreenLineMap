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

        try:
            while True:
                while not self.partying:
                    if not self.isPaused:

                        trains, stops = self.map.tick()
                        self.leds.tick(trains, stops)

                        textMap = self.map.textMap()

                    time.sleep(1)

                while self.partying:
                    if not self.isPaused:
                        self.leds.party()
                    else:
                        time.sleep(0.2)

        except KeyboardInterrupt:
            self.leds.pause()
            
    def pause(self):
        print("Pausing")
        self.isPaused = True
        self.leds.pause()

    def restart(self):
        print("Restarting")
        self.isPaused = False
        self.partying = False
        self.leds.interrupt = False

    def party(self):
        print("Partying")
        self.partying = True
        self.leds.interrupt = False

    def trains(self):
        print("Running trains")
        self.leds.pause()
        self.partying = False
        self.leds.interrupt = True