# main.py contains the controls necessary to start and stop the led program
from control import Controller
from server import *
from gpiozero import Button
import argparse
import logging


controller = Controller()


def restart():
    controller.restart()


def stop():
    controller.pause()


def togglePower(p):
    if p == "off":
        stop()
        return "Pausing LED Program"
    elif p == "on" and controller.isPaused:
        restart()
        return "Restarting LED Program"
    else :
        return "Already on"


def setMode(m):
    if m == "party":   
        controller.party()
        return "Partying"
    else:
        controller.trains()
        return "Tracking trains"


def toggleButton():
    if controller.isPaused:
        restart()
    elif controller.partying:
        stop()
    else:
        controller.party()


def run():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.WARNING)

    button = Button(21)
    button.when_pressed = toggleButton

    # setupServer(togglePower, setMode)
    
    try:
        controller.tick()
    
    except KeyboardInterrupt:
        controller.pause()
        logging.warning("Received keyboard interrupt, shutting down")

if __name__ == "__main__":
    run()