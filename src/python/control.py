# control.py is the main control center for the led program, viewed as a state machine
import var
import util
import map
import time
import logging


class Controller(object):

    def __init__(self):
        self.state = 0
        self.map = map.Lines()
        self.isPaused = False

    def getData(self):
        print(self.map.jsonify())
        return self.map.jsonify()

    def tick(self):

        while True:
            try: 
                if not self.isPaused:

                    self.map.tick()

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

    def trains(self):
        logging.info("Running trains")