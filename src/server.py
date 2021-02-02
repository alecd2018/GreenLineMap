# server.py launches a Python based server for starting and stopping the led program

from var import *
from flask import Flask, make_response
from threading import Thread
import logging
app = Flask(__name__)


def run():
    logging.info("Starting server at " + SERVER_IP)
    app.run(host=SERVER_IP, port=80)


toggle_cb = None


def setupServer(t,s):
    global toggle_cb
    global set_mode
    global thread 

    toggle_cb = t
    set_mode = s

    thread = Thread(target = run)
    thread.start()


@app.route("/toggle/<state>")
def toggle(state):
    return str(toggle_cb(state)).lower()


@app.route("/mode/<mode>")
def changeMode(mode):
    resp = set_mode(mode)
    return str(resp.lower())