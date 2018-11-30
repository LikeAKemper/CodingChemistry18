from dataCollector import *
from ML import *
from kNN import *
import os

def saveDataToJSON(pandasObject, name):
    f = open(name+'.json', 'w')
    f.write(pandasObject.to_json(orient='index'))

def saveDataToCSV(pandasObject, name):
    os.chdir('./WebsiteData/')
    f = open(name+'.csv', 'w')
    f.write(pandasObject.to_csv())
    os.chdir('..')

startTime = pd.to_datetime('2017-11-08 00:00')
endTime = pd.to_datetime('2017-11-18 00:00')
nHoursPredict = 10
lag = 11
nNearestNeighbor = 5
locations = [[49.496548, 8.585716], [49.487793, 8.592454],
             [49.498726, 8.593487], [49.498726, 8.593487]]
#locations = [[49.496548, 8.585716]]
dC = dataCollector()
for i, loc in enumerate(locations):
    response = dC.getHourlyHistoricData(loc, startTime, endTime)
    df = dataCollector.createPandas(response, loc, startTime, endTime)
    saveDataToJSON(df, "rawAPIdata "+ str(i))

for i, loc in enumerate(locations):
    dataName = "rawAPIdata "+str(i)+".json"
    NNR = kNN(dataName, lag, nNearestNeighbor)
    for hours in range(10):
        historicDF = NNR.giveLast24HistoricData()
        saveDataToCSV(historicDF, str(i)+str(hours)+'Historic')
        predDataKNN = NNR.predict(nHoursPredict)
        saveDataToCSV(predDataKNN, str(i)+str(hours)+'PredKNN')
        truePred = NNR.fullInformationForecast(nHoursPredict)
        saveDataToCSV(truePred, str(i)+str(hours)+'PredTrue')
        NNR.plot(nHoursPredict)
        NNR.step()
