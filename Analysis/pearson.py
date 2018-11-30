import pandas as pd
from ML import *
from dataCollector import *


class pearsonAnalysis:

    def __init__(self):
        MLobject = ML('PEARSON.json')
        dfWithLags, corr = MLobject.applyAnalysis(30)
        print(corr)
        return

    def loadDataFromAPI(self):
        startTime = pd.to_datetime('2017-11-30 00:00')
        endTime = pd.to_datetime('2017-12-10 00:00')
        loc = [49, 8]
        data = dataCollector()
        response = data.getHourlyHistoricData(loc, startTime, endTime)
        self.df = dataCollector.createPandas(response, loc, startTime, endTime)
        self.saveDataToJSON(self.df, 'pearsonCorrelationLARGE4.json')
        return

    def saveDataToJSON(self, pandasObject, name):
        f = open(name, "w")
        f.write(pandasObject.to_json(orient='index'))
        return

    def loadAndCreateNewJson(self, nDataSamples=4):
        frames = []
        for i in range(1,nDataSamples+1):
            f = open('pearsonCorrelationLARGE'+str(i)+'.json', 'r')
            string = f.read()
            pand = pd.read_json(string, orient='index')
            frames.append(pand)
        result = pd.concat(frames, keys=frames[0].columns)
        self.saveDataToJSON(result, 'PEARSON.json')
        return result
