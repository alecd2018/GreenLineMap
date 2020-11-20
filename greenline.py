import requests
import json
import datetime
import time

def getPredictionData():
    url = "https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=3&filter%5Bdirection_id%5D=1&filter%5Bstop%5D=place-stpul"
    resp = requests.get(url)

    data = json.loads(resp.text)

    return data["data"]

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

        # if (diffMinutes < 0 or (diffMinutes ==0 and diffSeconds <0)):

        absDiffMinutes = departTime.minute - datetime.datetime.now().minute
        absDiffSeconds = departTime.second - datetime.datetime.now().second
        diffMinutes = absDiffMinutes if (absDiffSeconds >= 0) else absDiffMinutes - 1
        diffSeconds = absDiffSeconds if (absDiffSeconds >= 0) else absDiffSeconds + 60 

        if diffMinutes >= 0:
            timeList.append("Leaving in "+str(diffMinutes) + "m"+ str(diffSeconds) + "s")

    print(timeList)

def run():
    while True:
        data = getPredictionData()
        listPredictTimes(data)
        time.sleep(10)

run()