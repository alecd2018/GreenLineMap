# server.py launches a Python based server for starting and stopping the led program

from var import *
from flask import Flask, make_response
from threading import Thread
import logging
app = Flask(__name__)


def run():
    print("Starting server at " + SERVER_IP+":"+str(PORT))
    app.run(host=SERVER_IP, port=PORT)


toggle_cb = None


def setupServer(t, g):
    global toggle_cb
    global getter
    global thread 

    toggle_cb = t
    getter = g

    thread = Thread(target = run)
    thread.start()


@app.route("/toggle/<state>")
def toggle(state):
    return str(toggle_cb(state)).lower()


@app.route("/data")
def getData():
    return getter()