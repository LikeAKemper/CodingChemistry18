import requests
import pandas as pd
import numpy as np
import os
import json

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
            "&start={}&end={}&location={}, {}&unitcode=si-std"
        startEpoch = int(startDateTime.timestamp())
        endEpoch = int(endDateTime.timestamp())
        requestUrl = url.format(dataCollector.APP_ID, dataCollector.APP_KEY, startEpoch,
                                endEpoch, location[0], location[1])
        response = self.session.get(requestUrl)
        jsonFileInput = response.json()
        dataCollector.createPandas(jsonFileInput, location, startDateTime, endDateTime)
        return jsonFileInput

    @staticmethod
    def createPandas(jsonFileInput, location, startDateTime, endDateTime):
        string = str(jsonFileInput[str(location[0])+','+str(location[1])])
        string = string.replace('hourly_historical:', '')
        #string = string.replace("{'unit': 'F', 'value':", '')
        js = json.dumps(eval(string))
        pand = pd.read_json(js, orient='index')
        pand.air_temp = pand.air_temp.apply(pd.Series).value
        pand.cloud_cover = pand.cloud_cover.apply(pd.Series).value
        pand.dew_point = pand.dew_point.apply(pd.Series).value
        pand.ice_acc_period = pand.ice_acc_period.apply(pd.Series).value
        pand.precip_acc_period_raw = pand.precip_acc_period_raw.apply(pd.Series).value
        pand.relative_humidity = pand.relative_humidity.apply(pd.Series).value
        pand.liquid_acc_period = pand.liquid_acc_period.apply(pd.Series).value
        pand.short_wave_radiation = pand.short_wave_radiation.apply(pd.Series).value
        pand.long_wave_radiation = pand.long_wave_radiation.apply(pd.Series).value
        pand.precip_acc_period = pand.precip_acc_period.apply(pd.Series).value
        pand.precip_acc_period_adjusted = pand.precip_acc_period_adjusted.apply(pd.Series).value
        pand.snow_acc_period = pand.snow_acc_period.apply(pd.Series).value
        pand.u_wind_speed = pand.u_wind_speed.apply(pd.Series).value
        pand.v_wind_speed = pand.v_wind_speed.apply(pd.Series).value
        #pand.valid_time_end = pand.valid_time_end.apply(pd.Series).value
        #pand.valid_time_start = pand.valid_time_start.apply(pd.Series).value
        pand.visibility = pand.visibility.apply(pd.Series).value
        pand.wind_direction = pand.wind_direction.apply(pd.Series).value
        pand.wind_gust = pand.wind_gust.apply(pd.Series).value
        pand.wind_speed = pand.wind_speed.apply(pd.Series).value
        pand.wind_speed_2m = pand.wind_speed_2m.apply(pd.Series).value

        listToDropAlways = {'descriptors', 'valid_time_end', 'valid_time_start', 'wind_gust'}
        listToDropAllButRain = {'air_temp', 'cloud_cover','dew_point', 'ice_acc_period',
                                'precip_acc_period_raw', 'relative_humidity', 'precip_acc_period',
                                'short_wave_radiation', 'long_wave_radiation', 'snow_acc_period',
                                'precip_acc_period_adjusted', 'u_wind_speed', 'v_wind_speed',
                                'visibility', 'wind_direction', 'wind_speed', 'wind_speed_2m'}
        unionSet = listToDropAlways.union(listToDropAlways)
        pand = pand.drop(columns=listToDropAlways)
        # os.chdir('./JsonFiles')
        # f = open(str(location)+'PEARSON.json', "w")
        # # f.write(pand.to_csv())
        # f.write(pand.to_json(orient='index'))
        # os.chdir('..')
        return pand


# startTime = pd.to_datetime('2017-11-01 00:00')
# endTime = pd.to_datetime('2017-12-10 00:00')
# MannheimLocation = [49, 8]
# data = dataCollector()
# response = data.getHourlyHistoricData(MannheimLocation, startTime, endTime)
# print(dataCollector.createPandas(response, MannheimLocation, startTime, endTime))
