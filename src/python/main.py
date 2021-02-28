# main.py contains the controls necessary to start and stop the led program
from control import Controller
from server import *
import argparse
import logging


controller = Controller()


def togglePower(p):
    if p == "off":
        controller.pause()
        return "Pausing LED Program"
    elif p == "on" and controller.isPaused:
        controller.restart()
        return "Restarting LED Program"
    else :
        return "Already on"


def toggleButton():
    if controller.isPaused:
        controller.restart()
    else:
        controller.pause()


def getData():
    return controller.getData()


def run():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.WARNING)

    setupServer(togglePower, getData)
    
    try:
        controller.tick()
    
    except KeyboardInterrupt:
        controller.pause()
        logging.warning("Received keyboard interrupt, shutting down")

if __name__ == "__main__":
    run()