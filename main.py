# main.py contains the controls necessary to start and stop the led program
from control import Controller
from server import *


controller = Controller()

# TODO: maybe make controller separate thread

def start():
    controller.tick()


def restart():
    controller.restart()
    controller.tick()


def stop():
    controller.pause()


def togglePower(p):
    print("STATE: "+p)
    print(controller.isPaused)
    if p == "off":
        stop()
        return "Pausing LED Program"
    elif p == "on" and controller.isPaused:
        restart()
        return "Restarting LED Program"
    else :
        return "Already on"


def run():
    setupServer(togglePower)
    start()


if __name__ == "__main__":
    run()