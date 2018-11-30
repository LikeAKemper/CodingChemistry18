import os
from ML import *
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt


class kNN:

    def __init__(self, nameOfDataSet, autoregressiveLag, nNeighbors, weights='distance'):
        self.nNeighbors = nNeighbors
        self.startingDelay = 24
        MLobject = ML(nameOfDataSet)

        originalDataSeries = MLobject.calculateLaggedInstance(autoregressiveLag)
        self.originalDataSeries = originalDataSeries
        self.df = originalDataSeries.iloc[0:-self.startingDelay]
        # self.saveDataToCSV(self.df.iloc[-24:, 0], 'historicData')
        self.futureData = originalDataSeries.iloc[-self.startingDelay:]
        return

    def step(self):
        self.startingDelay -= 1
        self.df = self.originalDataSeries.iloc[0:-self.startingDelay]
        self.futureData = self.originalDataSeries.iloc[-self.startingDelay:]
        return

    def fullInformationForecast(self, nHours=5):
        predictedTimeSeries = self.futureData.iloc[0:nHours, 0]
        return predictedTimeSeries

    def predict(self, nHours=5):
        Ycurrent = NNR.df.last('1h').iloc[:, 1:len(self.df.columns)-1].values
        Yold = NNR.df.iloc[0:-1, 1:len(self.df.columns)-1].values
        distMatrix = scipy.spatial.distance.cdist(Yold, Ycurrent)
        ikNearest = distMatrix.flatten().argsort()[:self.nNeighbors]
        iPredValues = ikNearest.T + np.arange(1, len(ikNearest) + 1)
        kNearestPredValues = Yold[iPredValues]
        prediction = (1/self.nNeighbors)*kNearestPredValues.sum(axis=0)[0:nHours]
        preTime = self.df.index[-1] + pd.timedelta_range(start='1 hours', periods=nHours, freq='h')
        predTS = pd.DataFrame(prediction, index=preTime)
        # self.saveDataToCSV(predTS.iloc[:, :], 'prediction')
        return predTS

    def plot(self, nHoursHistory=24):
        historicData = self.df.iloc[-nHoursHistory:, 0]
        predictionKNN = self.predict()
        predictionFullInformation = self.fullInformationForecast()
        a = historicData.plot(style=['b-o'], label='historic data')
        predictionKNN.plot(ax=a, style=['r-.'], label='prediction kNN')
        predictionFullInformation.plot(ax=a, style=['--'], label='truth')
        plt.legend(loc='upper left')
        plt.show()
        return

    def runSimulation(self):
        while self.startingDelay > 0:
            self.plot()
            self.step()
        return

    def saveDataToCSV(self, pandasObject, name):
        f = open(name+'.csv', 'w')
        f.write(pandasObject.to_csv())
        return


nameOfDataSet = '[49, 8]onlyRain.json'
lag = 10
nNeighbors = 5
NNR = kNN(nameOfDataSet, lag, nNeighbors)
