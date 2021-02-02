# control.py is the main control center for the led program, viewed as a state machine
import var
import util
import map
import time
import logging


class Controller(object):

    def __init__(self):
        self.state = 0
        self.map = map.Map()
        self.isPaused = False
        self.partying = False

    def tick(self):

        while True:
            try: 
                if not self.isPaused:

                    trains, stops = self.map.tick()

                    textMap = self.map.textMap()
                    logging.debug(textMap)
                    print(textMap)

                time.sleep(1)

            except ConnectionError:
                # wait 5 seconds, then try again
                logging.error("Connection error, retrying in 5 seconds...")
                time.sleep(5)
            
    def pause(self):
        logging.info("Pausing")
        self.isPaused = True

    def restart(self):
        logging.info("Restarting")
        self.isPaused = False
        self.partying = False

    def party(self):
        logging.info("Partying")
        self.partying = True

    def trains(self):
        logging.info("Running trains")
        self.partying = False