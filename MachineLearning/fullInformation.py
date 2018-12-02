import random
from ML import *
import pandas as pd
import matplotlib.pyplot as plt


class fullInformation:

    """
    forecaster with full information
    """

    def __init__(self, initalDateTime, fullTimeSeries, nameOfDataSet):
        MLobject = ML(nameOfDataSet)
        self.currentDateTime = initalDateTime
        self.originalData = fullTimeSeries
        self.historicData = fullTimeSeries[fullTimeSeries.index <= self.currentDateTime]

    def predict(self, nHours=5):
        predictionHorizon = pd.Timedelta(str(nHours) +' hours')
        futureTime = self.currentDateTime + predictionHorizon
        untilFutureTS = self.originalData[self.originalData.index <= futureTime]
        predictedTimeSeries = untilFutureTS[untilFutureTS.index >= self.currentDateTime]
        return predictedTimeSeries

    def step(self, currentDateTime):
        assert (currentDateTime > self.currentDateTime), "Current Datetime older than expected"
        self.historicData = self.historicData.append(self.getCurrentSeries())
        self.currentDateTime = currentDateTime
        return

    def getCurrentSeries(self):
        indexCurrentValue = self.originalData.index.get_loc(self.currentDateTime, 'nearest')
        currentValue = self.originalData[indexCurrentValue]
        currentTS = pd.Series(currentValue, index=[self.currentDateTime])
        return currentTS

    def plot(self):
        resampledTS = self.historicData.resample(self.samplingRate).mean()
        resampledTS = resampledTS.append(self.getCurrentSeries())
        a = resampledTS.plot(style=['b-o'], label='historic data resampled')

        indicesHistoricOriginal = self.originalData.index <= self.currentDateTime
        self.originalData[indicesHistoricOriginal].plot(ax=a, style=['r-.'], label='original')
        predictedTimeSeries = self.predict()
        predictedTimeSeries.plot(ax=a, style=['g'], label='prediction')
        plt.legend(loc='upper left')

        plt.plot_date([self.currentDateTime, self.currentDateTime], a.get_ylim(), fmt='-.')
        plt.show()

    @classmethod
    def sampleFullInfo(cls):
        pass

currentTimeString = '2017-07-11'
currentDateTime = pd.to_datetime(currentTimeString, format='%Y-%m-%d %H:%M')
fullInfo = fullInformation(currentDateTime, timeSeries)
