# server.py launches a Python based server for starting and stopping the led pr

from var import *
from flask import Flask, make_response
from threading import Thread
app = Flask(__name__)


def run():
    print("Starting server at " + SERVER_IP)
    app.run(host=SERVER_IP, port=80)


toggle_cb = None
# brightness_cb = None


def setupServer(t,s):
    global toggle_cb
    global set_mode
    # global brightness_cb
    toggle_cb = t
    set_mode = s

    # brightness_cb = b
    # _thread.start_new_thread(run, ())
    thread = Thread(target = run)
    thread.start()


@app.route("/toggle/<state>")
def toggle(state):
    return str(toggle_cb(state)).lower()


@app.route("/mode/<mode>")
def changeMode(mode):
    resp = set_mode(mode)
    return str(resp.lower())