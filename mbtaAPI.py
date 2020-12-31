# mbtaAPI.py is a file exclusively to read and process data from the MBTA API
import requests
import json
import logging
from var import *


def getRequest(method, parameters=None):
    parameters = parameters or {}
    parameters['api_key'] = API_KEY
    # parameters['format'] = 'json'
    data = json.loads(requests.get(
        MBTA_BASE_URL + method,
        params=parameters
    ).text)
    return data


def getTrains():
    try:
        # Get trains going into Boston
        data = getRequest("vehicles", {"filter[route]": ROUTE, "filter[direction_id]": 1})
        return data
    except Exception:
        logging.error("Train request failed")


def getStops():
    try:
        data = getRequest("stops", {"filter[route]" : ROUTE})
        return data
    except Exception:
        logging.error("Stops request failed")


def getPrediction(stopID):
    try:
        data = getRequest("predictions", {"page[limit]" : 3, "filter[route]" : ROUTE, "filter[stop]" : stopID})
        return data
    except Exception:
        logging.error("Predictions request failed")