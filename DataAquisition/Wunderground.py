from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt


class Wunderground:

    def __init__(self):
        self.keys = ["90d772fad48e1e11", "f85b650e1cbaebb8", "96eef3bc9d88fa26"]
        self.keyUseCount = 0
        self.numKeys = len(self.keys)

    def runLoop(self):
        target_date = datetime(2016, 5, 16)
        features = ["date", "meantempm", "meandewptm", "meanpressurem", "maxhumidity",
            "minhumidity", "maxtempm",  "mintempm", "maxdewptm", "mindewptm", "maxpressurem",
            "minpressurem", "precipm"]
        self.DailySummary = namedtuple("DailySummary", features)
        BASE_URL = "http://api.wunderground.com/api/{}/history_{}/q/NE/Lincoln.json"
        records = self.extract_weather_data(BASE_URL, target_date, 10)
        df = pd.DataFrame(records, columns=features).set_index('date')
        return df

    def extract_weather_data(self, url, target_date, days):
        records = []
        for _ in range(days):
            api_key = self.keys[self.keyUseCount%self.numKeys]
            self.keyUseCount+=1
            request = url.format(api_key, target_date.strftime('%Y%m%d'))
            response = requests.get(request)
            if response.status_code == 200:
                data = response.json()['history']['dailysummary'][0]
                records.append(self.DailySummary(
                    date=target_date,
                    meantempm=data['meantempm'],
                    meandewptm=data['meandewptm'],
                    meanpressurem=data['meanpressurem'],
                    maxhumidity=data['maxhumidity'],
                    minhumidity=data['minhumidity'],
                    maxtempm=data['maxtempm'],
                    mintempm=data['mintempm'],
                    maxdewptm=data['maxdewptm'],
                    mindewptm=data['mindewptm'],
                    maxpressurem=data['maxpressurem'],
                    minpressurem=data['minpressurem'],
                    precipm=data['precipm']))
            time.sleep(1)
            target_date += timedelta(days=1)
        return records

WI = Wunderground()
df = WI.runLoop()
