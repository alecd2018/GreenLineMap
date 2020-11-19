import requests
import json
import datetime

url = "https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=3&filter%5Bdirection_id%5D=1&filter%5Bstop%5D=place-stpul"
resp = requests.get(url)

data = json.loads(resp.text)

trainList = data["data"]

if (len(trainList) == 0):
    print("No trains")
elif (len(trainList) == 1):
    trainArrival0 = trainList[0]["attributes"]["arrival_time"]
    arrvialTime0 = datetime.datetime.strptime(trainArrival0, '%Y-%m-%dT%H:%M:%S-5:00')
    arrvialTime0 = arrvialTime0.time()
else:
    trainArrival0 = trainList[0]["attributes"]["arrival_time"]
    arrvialTime0 = datetime.datetime.strptime(trainArrival0, '%Y-%m-%dT%H:%M:%S-5:00')
    arrvialTime0 = arrvialTime0.time()

    print(arrvialTime0)