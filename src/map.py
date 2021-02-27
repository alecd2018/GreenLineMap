import mbtaAPI
import util
import datetime
import logging
import time

from var import *

class Lines(object):

    def __init__(self):
        self.lines = []
        for line in LINE_LIST:
            self.lines.append(Line(line))

    def tick(self):
        print('')
        for line in self.lines:
            trains, stops = line.tick()

            textMap = line.textMap()
            logging.debug(textMap)
            print(textMap)

class Line(object):

    def __init__(self, name):
        self.name = name
        self.trains = {}
        self.stops = Stops(self.name)

    def tick(self):
        self.trains = Trains(self.stops.sortedStops)

        self.trains.update(self.name, self.stops.stops)

        return (self.trains, self.stops)

    def marker(self, i):
        if self.trains.get(i) and len(self.trains.get(i)):
            flags = [False, False]
            for t in self.trains.get(i):
                flags[t.direction] = True
            if flags[0] and flags[1]:
                return 'X' if self.stops.get(i) else 'x'
            elif flags[0]:
                return '(' if self.stops.get(i) else '<'
            else:
                return ')' if self.stops.get(i) else '>'
        if self.stops.get(i):
            return 'o'
        else:
            return '-'

    def textMap(self):
        return self.name + ' ' + ''.join(map(self.marker, range(TOTAL_NUM_PIXELS)))


class Stop(object):

    def __init__(self, id, name, location):
        self.name = name
        self.location = location
        self.pixelLocation = -1
        self.id = id

    def __str__(self):
        return '{'+self.name+', '+str(self.pixelLocation)+'}'
        

class Stops(object):

    def __init__(self, name):
        self.stops = {}
        self.sortedStops = []
        self.pixelList = []
        for i in range(TOTAL_NUM_PIXELS):
            self.pixelList.append([])

        # get API data on stops
        resp = None
        errorRecoveryTime = 5
        while resp is None:
            try:
                resp = mbtaAPI.getStops(name)['data']
            except Exception:
                logging.error("Failed to get stops, trying again in "+str(errorRecoveryTime)+" seconds")
                time.sleep(errorRecoveryTime)
                if (errorRecoveryTime > 60 and errorRecoveryTime != 3600):
                    errorRecoveryTime = 3600
                else:
                    errorRecoveryTime += 5

        # init stops
        for stop in resp:
            lat = stop['attributes']['latitude']
            lon = stop['attributes']['longitude']
            loc = (lat, lon)
            stopObj = Stop(stop['id'], stop["attributes"]['name'], loc)
            self.stops[stop['id']] = stopObj
            self.sortedStops.append(stop['id'])

        # get total Dist from end to end
        totalDist = 0
        for i in range(len(self.sortedStops)-1):
            stopA = self.stops[self.sortedStops[i]]
            stopB = self.stops[self.sortedStops[i+1]]
            totalDist += util.distTwoPoints(stopA.location, stopB.location)

        # initialize pixel list of stops
        for i in range(len(self.sortedStops)-1):
            stopA = self.stops[self.sortedStops[i]]
            stopB = self.stops[self.sortedStops[i+1]]
            dist = util.distTwoPoints(stopA.location, stopB.location)

            if i == 0:
                stopA.pixelLocation = 0

            pixDist = round(TOTAL_NUM_PIXELS * dist / totalDist)
            stopB.pixelLocation = stopA.pixelLocation + pixDist 
            if stopB.pixelLocation >= TOTAL_NUM_PIXELS:
                 stopB.pixelLocation = TOTAL_NUM_PIXELS - 1

            self.pixelList[stopB.pixelLocation].append(stopB)

    def __str__(self):
        res = ""
        for stop in self.stops:
            res += str(self.stops[stop])+'\n'
        return res

    # used for LED version
    def filterAbbrStops(self, resp):
        abbrList = []
        for stop in resp:
            if stop['id'] in self.sortedStops:
                abbrList.append(stop)
        return abbrList

    def get(self, i):
        return self.pixelList[i]

            
class Train(object):

    def __init__(self, location, direction, timestamp):
        self.location = location
        self.direction = direction
        self.prev = ""
        self.next = ""
        self.timestamp = timestamp

    def __str__(self):
        return "{"+str(self.location)+', '+str(self.direction)+', '+str(self.prev)+', '+str(self.next)+'}'


class Trains(object):

    def __init__(self, sortedStops):
        self.trains = {}
        self.pixelList = []
        self.sortedStops = sortedStops
        for i in range(TOTAL_NUM_PIXELS):
            self.pixelList.append([])

    def __str__(self):
        res = ""
        for t in self.trains:
            res += str(self.trains[t]) + '\n'

        for p in self.pixelList:
            res += str(p)
        return res
        
    def get(self, i):
        return self.pixelList[i]

    def getPrediction(self, id):
        resp = mbtaAPI.getPrediction(id)
        l = []
        for train in resp['data']:  
            l.append(train['attributes']['arrival_time'])
        print(l)
        return l

    def getTrainPixel(self, train):
        prevStop = train.prev.location
        nextStop = train.next.location
        distPrev = util.distTwoPoints(train.location, prevStop)
        distSegment = util.distTwoPoints(nextStop, prevStop)

        prevPixel = train.prev.pixelLocation
        nextPixel = train.next.pixelLocation
        segmentPixels = nextPixel - prevPixel
        pixel = round(segmentPixels * distPrev / distSegment) + prevPixel

        if pixel >= TOTAL_NUM_PIXELS:
            pixel = TOTAL_NUM_PIXELS - 1

        return pixel

    def filterAbbrTrains(self, stops):
        abbrTrains = {}
        for train in self.trains:
            t = self.trains[train]
            if t.next.id in self.sortedStops[1:]:
                t.next = stops[t.next.id]
                t.prev = stops[t.prev.id]
                abbrTrains[train] = t
            elif t.prev.id in self.sortedStops[:-1]:
                t.next = stops[t.next.id]
                t.prev = stops[t.prev.id]
                abbrTrains[train] = t
        return abbrTrains
    
    def update(self, name, stops):
        errorRecoveryTime = 5
        resp = None
        while resp is None:
            try:
                resp = mbtaAPI.getTrains(name)['data']
            except Exception:
                logging.error("Failed to get trains, trying again in "+str(errorRecoveryTime)+" seconds")
                time.sleep(errorRecoveryTime)
                if (errorRecoveryTime > 60 and errorRecoveryTime != 3600):
                    errorRecoveryTime = 3600
                else:
                    errorRecoveryTime += 5

        self.pixelList = []
        for i in range(TOTAL_NUM_PIXELS):
            self.pixelList.append([])
        
        oldLoc = 0
        oldTime = 0
        for train in resp:

            if train['id'] in self.trains:
                oldLoc = self.trains[train['id']].location
                oldTime = self.trains[train['id']].timestamp

            lat = train['attributes']['latitude']
            lon = train['attributes']['longitude']
            loc = (lat, lon)
            timestamp = datetime.datetime.now()
            status = train['attributes']['current_status']

            t = Train(loc, train['attributes']['direction_id'], timestamp)
            self.trains[train['id']] = t

        for train in self.trains:
            closest = ("", "")
            minDist = 10000
            for i in range(len(self.sortedStops)-1):
                t = self.trains[train]
                stopA = stops[self.sortedStops[i]]
                stopB = stops[self.sortedStops[i+1]]
                distToSegment = util.distPointLine(t.location, stopA.location, stopB.location)

                if distToSegment < minDist:
                    minDist = distToSegment
                    # closest = (stopA, stopB) if t.direction == 1 else (stopB, stopA)
                    closest = (stopA, stopB)

            t.prev = closest[0]
            t.next = closest[1]

        self.pointUpdate()

    def pointUpdate(self):

        for train in self.trains:
            
            pixel = self.getTrainPixel(self.trains[train])

            self.pixelList[pixel].append(self.trains[train])
