import requests
import json
import datetime
import time
import json
import math

NUM_PIXELS = 10
API_KEY = '48a3fb6b1cd34f7b859d0e0d220c15d1'

def getRequest(url):
    headers = {"x-api-key": API_KEY}
    resp = requests.get(url, headers=headers)
    # print(resp.headers)
    return json.loads(resp.text)

def lookup(id, inList):
    for item in inList:
        if item["id"] == id:
            return item

def getDistance(x1, y1, x2, y2):
    return math.sqrt((float(x2) - float(x1))**2 + (float(y2) - float(y1))**2)

def getClosestStops(x, y, stops, noStop="none", secNoStop="none"):
    minDist = 100
    minStop = ""
    for stop in stops:
        d = getDistance(x, y, stops[stop]["lat"], stops[stop]["lon"])
        if d < minDist and stop!=noStop and stop!=secNoStop:
            minStop = stop
            minDist = d
    return stops[minStop]

# Get slope line between two points
def getSlope(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m*x1
    return (m, b)

# Create new point on a line by transposing a point to a line
def transpose(x1, y1, x2, y2):
    line = getSlope(x1, y1, x2, y2)

    perpB = y1 + line[0] * x1
    perpBSlope = (-line[0] , perpB)
    transposedXCoord = (perpBSlope[1] - line[1]) / (line[0] - perpBSlope[0])
    transposedYCoord = (line[0] * transposedXCoord) + line[1]
    return (transposedXCoord, transposedYCoord)

def getNextStop(train, stopA, stops):
    stopBID = stopA['prevStop']
    stopCID = stopA['nextStop']

    if stopCID == "":
        return ""

    if stopBID == "":
        return stops[stopA['nextStop']]
    else:
        stopB = stops[stopBID]

        distAB = getDistance(stopA['lat'], stopA['lon'], stopA['lat'], stopB['lon'])
        distBTrain = getDistance(train['lat'], train['lon'], stopB['lat'], stopB['lon'])

        if distAB < distBTrain:
            return stops[stopA['nextStop']]
        else:
            return stopA

# Convert line location to pixel light up
def getPixel(point, closest, nextStop):

    # TODO: fix next stop estimator

    distStops = getDistance(closest['lat'], closest['lon'], nextStop['lat'], nextStop['lon'])
    distPerPixel = distStops / NUM_PIXELS

    distToClosestStop = getDistance(point[0], point[1], closest['lat'], closest['lon'])
    dist2 = getDistance(point[0], point[1], nextStop['lat'], nextStop['lon'])

    bucket = distToClosestStop / distPerPixel
    print(bucket)
    bucketCount = 0
    for b in range(NUM_PIXELS):
        if bucket > -0.5 and bucket < 0.5:
            return bucketCount
        else:
            bucket -= 1
            bucketCount += 1

    return

def getPixelList(stops):
    stopPixels = [None] * (len(stops) * NUM_PIXELS)
    i = 0
    for stop in stops:
        stopPixels[i] = stop
        for j in range(NUM_PIXELS-1):
            stopPixels[i+j + 1] = ''
        i += NUM_PIXELS
    return stopPixels

def getStopsData():
    data = {}
    with open("stops.json") as respFile:
        data = json.load(respFile)

    stops = {}
    pixelCount = 0
    prevStop = ""
    for stop in data["data"]:
        newStop = {}
        newStop['id'] = stop['id']
        newStop["lat"] = stop["attributes"]["latitude"]
        newStop["lon"] = stop["attributes"]["longitude"]
        newStop["name"] = stop['attributes']["name"]
        newStop['pixelNumber'] = pixelCount
        pixelCount += NUM_PIXELS
        newStop['prevStop'] = prevStop
        newStop['nextStop'] = ''
        if prevStop != '':
            stops[prevStop]['nextStop'] = stop['id']
        prevStop = stop['id']
        stops[stop['id']] = newStop
    return stops

def getTrainData():
    #TODO: filter direction
    url = "https://api-v3.mbta.com/vehicles?page%5Boffset%5D=0&include=stop&filter%5Broute%5D=Green-C&filter%5Bdirection_id%5D=1"
    
    data = getRequest(url)

    trains = []
    for train in data["data"]:
        newTrain = {}
        newTrain["id"] = train["id"]
        newTrain["lat"] = train["attributes"]["latitude"]
        newTrain["lon"] = train["attributes"]["longitude"]
        trains.append(newTrain)
    
    return trains


def listPredictTimes(trainList):
    timeList = []
    for train in trainList:
        trainArrival = train["attributes"]["arrival_time"]
        arrivalTime = datetime.datetime.strptime(trainArrival, '%Y-%m-%dT%H:%M:%S-05:00') 
        trainDeparture = train["attributes"]["departure_time"]
        departTime = datetime.datetime.strptime(trainDeparture, '%Y-%m-%dT%H:%M:%S-05:00') 

        absDiffMinutes = arrivalTime.minute - datetime.datetime.now().minute
        absDiffSeconds = arrivalTime.second - datetime.datetime.now().second
        diffMinutes = absDiffMinutes if (absDiffSeconds >= 0) else absDiffMinutes - 1
        diffSeconds = absDiffSeconds if (absDiffSeconds >= 0) else absDiffSeconds + 60 

        if diffMinutes >= 0:
            timeList.append("Arriving in "+str(diffMinutes) + "m"+ str(diffSeconds) + "s")

        absDiffMinutes = departTime.minute - datetime.datetime.now().minute
        absDiffSeconds = departTime.second - datetime.datetime.now().second
        diffMinutes = absDiffMinutes if (absDiffSeconds >= 0) else absDiffMinutes - 1
        diffSeconds = absDiffSeconds if (absDiffSeconds >= 0) else absDiffSeconds + 60 

        if diffMinutes >= 0:
            timeList.append("Leaving in "+str(diffMinutes) + "m"+ str(diffSeconds) + "s")

    print(timeList)


def run():

    stops = getStopsData()
    print(stops)

    # TODO: initialize distance between stops to be standard pixel distance
    while True:
        # url = "https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=3&filter%5Bdirection_id%5D=1&filter%5Bstop%5D=place-stpul"
        # data = getRequest(url)['data']
        # listPredictTimes(data)

        pixelList = getPixelList(stops)

        trains = getTrainData()

        for train in trains:
            closest = getClosestStops(train["lat"], train["lon"], stops)
            print(closest)

            bestPoint = (train['lat'], train['lon'])
            nextStop = getNextStop(train, closest, stops)

            if nextStop != "":
                # bestPoint = transpose(closest["lat"], closest['lon'], secondClosest['lat'], secondClosest['lon'])

                if nextStop != closest:
                    pixel = getPixel(bestPoint, closest, nextStop)
                    pixel += stops[closest['id']]['pixelNumber']
                else:
                    pixel = getPixel(bestPoint, closest, stops[closest['prevStop']])
                    pixel = stops[closest['id']]['pixelNumber'] - pixel

                pixelList[pixel] += "X"

        print(pixelList)
        print('')

        time.sleep(2)


run()

# stops
# curl -X GET "https://api-v3.mbta.com/stops?page%5Boffset%5D=0&page%5Blimit%5D=20&filter%5Broute%5D=Green-C" -H "accept: application/vnd.api+json"

#vehicels
# curl -X GET "https://api-v3.mbta.com/vehicles?page%5Boffset%5D=0&page%5Blimit%5D=4&include=stop&filter%5Broute%5D=Green-C" -H "accept: application/vnd.api+json"