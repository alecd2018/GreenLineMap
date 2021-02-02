# control.py is the main control center for the led program, viewed as a state machine
import var
import util
import map
import time
import ledControl
import logging


class Controller(object):

    def __init__(self):
        self.state = 0
        self.map = map.Map()
        self.leds = ledControl.LEDControl()
        self.isPaused = False
        self.partying = False

    def tick(self):

        while True:
            try: 
                while not self.partying:
                    if not self.isPaused:

                        trains, stops = self.map.tick()
                        self.leds.tick(trains, stops)

                        textMap = self.map.textMap()
                        logging.debug(textMap)

                    time.sleep(1)

                while self.partying:
                    if not self.isPaused:
                        self.leds.party()
                    else:
                        time.sleep(0.2)

            except ConnectionError:
                # wait 5 seconds, then try again
                logging.error("Connection error, retrying in 5 seconds...")
                time.sleep(5)
            
    def pause(self):
        logging.info("Pausing")
        self.isPaused = True
        self.leds.pause()

    def restart(self):
        logging.info("Restarting")
        self.isPaused = False
        self.partying = False
        self.leds.interrupt = False

    def party(self):
        logging.info("Partying")
        self.partying = True
        self.leds.interrupt = False

    def trains(self):
        logging.info("Running trains")
        self.leds.pause()
        self.partying = False
        self.leds.interrupt = True