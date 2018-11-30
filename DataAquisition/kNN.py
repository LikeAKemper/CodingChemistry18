import os
from ML import *
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt


class kNN:

    def __init__(self, nameOfDataSet, autoregressiveLag, nNeighbors, startingDelay=64):
        self.nNeighbors = nNeighbors
        self.startingDelay = startingDelay
        self.lag = autoregressiveLag
        MLobject = ML(nameOfDataSet)

        originalDataSeries = MLobject.calculateLaggedInstance(self.lag)
        self.originalDataSeries = originalDataSeries
        self.df = originalDataSeries.iloc[0:-self.startingDelay]
        self.futureData = originalDataSeries.iloc[-self.startingDelay:]
        return

    def giveLast24HistoricData(self):
        fileToSave = self.df.iloc[-self.startingDelay:, 0]
        return fileToSave

    def step(self):
        self.startingDelay -= 1
        self.df = self.originalDataSeries.iloc[0:-self.startingDelay]
        self.futureData = self.originalDataSeries.iloc[-self.startingDelay:]
        return

    def fullInformationForecast(self, nHours=5):
        predictedTimeSeries = self.futureData.iloc[0:nHours, 0]
        return predictedTimeSeries

    def predict(self, nHours):
        assert (nHours < self.lag),'you are an idiot!'
        Ycurrent = self.df.last('1h').iloc[:, 1:len(self.df.columns)-1].values
        Yold = self.df.iloc[0:-1, 1:len(self.df.columns)-1].values
        distMatrix = scipy.spatial.distance.cdist(Yold, Ycurrent)
        ikNearest = distMatrix.flatten().argsort()[:self.nNeighbors]
        kNearestPredValues = Yold[ikNearest]
        # weights = distMatrix.flatten()[ikNearest]
        # weights[weights > 0] = 1/weights[weights > 0]
        # weights[weights == 0] = 1
        # weights = np.repeat(np.expand_dims(weights, axis=0), nHours, axis = 0)
        # print(weights)
        # print(weights, kNearestPredValues)
        # prediction = (1/self.nNeighbors)*(weights.T*kNearestPredValues).sum(axis=0)[0:nHours]
        prediction = (1/self.nNeighbors)*(kNearestPredValues.sum(axis=0)[0:nHours])
        preTime = self.df.index[-1] + pd.timedelta_range(start='1 hours', periods=nHours, freq='h')
        predTS = pd.DataFrame(prediction, index=preTime)
        # self.saveDataToCSV(predTS.iloc[:, :], 'prediction')
        return predTS

    def plot(self, nHoursPredict, nHoursHistory=24,):
        historicData = self.df.iloc[-nHoursHistory:, 0]
        predictionKNN = self.predict(nHoursPredict)
        predictionFullInformation = self.fullInformationForecast(nHoursPredict)
        a = historicData.plot(style=['b-o'], label='historic data')
        predictionKNN.plot(ax=a, style=['r-.'], label='prediction kNN')
        predictionFullInformation.plot(ax=a, style=['--'], label='truth')
        plt.legend(loc='upper left')
        plt.show()

    def calculateLMSE(self, nHoursPred, stepsToCalculate):
        LMSE = 0
        for i in range(stepsToCalculate):
            truePred = self.fullInformationForecast(nHoursPred).iloc[:].values.flatten()
            knnPred = self.predict(nHoursPred).iloc[:].values.flatten()
            LMSE = LMSE + (1/len(truePred))*np.sum((truePred-knnPred)**2)
        return LMSE

    def runSimulation(self):
        while self.startingDelay > 0:
            self.plot()
            self.step()
        return

    def saveDataToCSV(self, pandasObject, name):
        f = open(name+'.csv', 'w')
        f.write(pandasObject.to_csv())
