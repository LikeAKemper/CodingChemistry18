import pandas as pd
from ML import *
from dataCollector import *


class pearsonAnalysis:

    def __init__(self):
        # MLobject = ML('PEARSON.json')
        # dfWithLags, corr = MLobject.applyAnalysis(30)
        # print(corr)
        return

    def loadDataFromAPI(self, startTime, endTime, i):
        loc = [49.496548, 8.585716]
        data = dataCollector()
        response = data.getHourlyHistoricData(loc, startTime, endTime)
        self.df = dataCollector.createPandas(response, loc, startTime, endTime)
        self.saveDataToJSON(self.df, 'temp' + str(i) +'.json')
        return

    def saveDataToJSON(self, pandasObject, name):
        f = open(name, "w")
        f.write(pandasObject.to_json(orient='index'))
        return

    def loadAndCreateNewJson(self, nDataSamples=4):
        frames = []
        for i in range(1,nDataSamples+1):
            f = open('temp'+str(i)+'.json', 'r')
            string = f.read()
            pand = pd.read_json(string, orient='index')
            frames.append(pand)
        result = pd.concat(frames, keys=frames[0].columns)
        self.saveDataToJSON(result, '01dataSet.json')
        return result

PA = pearsonAnalysis()
startTime = [pd.to_datetime('2017-11-01 00:00'), pd.to_datetime('2017-11-10 00:00'),
             pd.to_datetime('2017-11-19 00:00'), pd.to_datetime('2017-11-28 00:00'),
             pd.to_datetime('2017-12-03 00:00'), pd.to_datetime('2017-12-12 00:00'),
             pd.to_datetime('2017-12-21 00:00')]
endTime = [pd.to_datetime('2017-11-10 00:00'), pd.to_datetime('2017-11-19 00:00'),
           pd.to_datetime('2017-11-28 00:00'), pd.to_datetime('2017-12-03 00:00'),
           pd.to_datetime('2017-12-12 00:00'), pd.to_datetime('2017-12-21 00:00'),
           pd.to_datetime('2017-12-31 00:00'),]
lag = 11
for i in range(len(startTime)):
    PA.loadDataFromAPI(startTime[i], endTime[i], )
result = PA.loadAndCreateNewJson()
