import requests
import pandas as pd
import numpy as np
import os


class dataCollector:
    """
    scrapes data from ClearAg API, converts it and stores it
    """

    APP_ID = '521aaaff'
    APP_KEY = 'f37946b7e0916dfe695b916e47d90e72'

    def __init__(self):
        self.session = requests.Session()

    def getCurrentConditions(self, location):
        url = "https://ag.us.clearapis.com/v1.1/currentconditions?app_id=" \
            "{}&app_key={}&location={},{}&unitcode=us-std&lang=en-us" \
            "&icon_resolution=128"
        requestUrl = url.format(dataCollector.APP_ID, dataCollector.APP_KEY, location[0],
                                 location[1])
        response = self.session.get(requestUrl).text

    def getDailyHistoricData(self, location, startDateTime, endDateTime):
        url = "https://ag.us.clearapis.com/v1.2/historical/daily?app_id={}&" \
            "app_key={}&start={}&end={}&location={},{}"
        startEpoch = int(startDateTime.timestamp())
        endEpoch = int(endDateTime.timestamp())
        requestUrl = url.format(dataCollector.APP_ID, dataCollector.APP_KEY, startEpoch,
                                endEpoch, location[0], location[1])
        response = self.session.get(requestUrl)
        return response.json()

    def getHourlyHistoricData(self, location, startDateTime, endDateTime):
        url = "https://ag.us.clearapis.com/v1.1/historical/hourly?app_id={}&app_key={}"\
            "&start={}&end={}&location={}, {}"
        startEpoch = int(startDateTime.timestamp())
        endEpoch = int(endDateTime.timestamp())
        requestUrl = url.format(dataCollector.APP_ID, dataCollector.APP_KEY, startEpoch,
                                endEpoch, location[0], location[1])
        response = self.session.get(requestUrl)
        os.chdir('./JsonFiles')
        jsonFileInput = response.json()
        f = open(str(location)+'.json', "w")
        f.write(str(jsonFileInput))
        os.chdir('..')
        return jsonFileInput




startTime = pd.to_datetime('2018-11-01 00:00')
endTime = pd.to_datetime('2018-11-02 00:00')

MannheimLocation = [49, 8]

data = dataCollector()

for i in range(100):
    response = data.getHourlyHistoricData(MannheimLocation, startTime, endTime)

# s = requests.Session()
# s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('https://httpbin.org/cookies').text
# print(r)
