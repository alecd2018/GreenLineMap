# main.py contains the controls necessary to start and stop the led program
from control import Controller
from server import *


controller = Controller()


def start():
    controller.tick()


def stop():
    controller.pause()


def run():
    setupServer(start, stop)
    start()


if __name__ == "__main__":
    run()