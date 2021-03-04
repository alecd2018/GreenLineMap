# server.py launches a Python based server for starting and stopping the led program

from var import *
from flask import Flask, render_template, jsonify
# from flask_cors import CORS
from threading import Thread
import logging
app = Flask(__name__)


def run():
    print("Starting server at " + SERVER_IP+":"+str(PORT))
    app.run(host=SERVER_IP, port=PORT)


def setupServer(t, g):
    global toggle_cb
    global getter
    global thread 

    toggle_cb = t
    getter = g

    thread = Thread(target = run)
    thread.start()

@app.route("/")
def serveHTML():
    return render_template("index.html")


@app.route("/toggle/<state>")
def toggle(state):
    return str(toggle_cb(state)).lower()


@app.route("/data", methods=['GET'])
def getData():
    data = getter()
    return jsonify(data)