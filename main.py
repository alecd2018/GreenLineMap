# main.py contains the controls necessary to start and stop the led program
from control import Controller
from server import *
from gpiozero import Button


controller = Controller()

def start():
    controller.tick()


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
    else:
        stop()


def run():

    button = Button(21)
    button.when_pressed = toggleButton

    setupServer(togglePower, setMode)
    start()


if __name__ == "__main__":
    run()