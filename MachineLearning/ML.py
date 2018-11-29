import os
import pandas as pd


class ML:

    def __init__(self, fileName):
        os.chdir('../DataAquisition/JsonFiles')
        f = open(fileName, 'r')
        str = f.read()
        os.chdir('../../MachineLearning')
        self.pand = pd.read_json(str, orient='index')
        return

    def calculateLaggedInstance(self, lag, targetFeature='precip_acc_period'):
        """
        for each day (row) and for a given feature (column) add value for that feature N days
        prior
        For each value of N (1-3 in our case) a new column is added for that feature representing
        the Nth prior day's measurement.
        @pararms:           targetFeature          'precip_acc_period'
        """
        features = self.pand.columns
        for feature in features:
            if feature != 'date':
                for N in range(1, lag + 1):
                    self.deriveNthDayFeature(N, feature)
        return

    def deriveNthDayFeature(self, N, feature='precip_duration'):
        # total number of rows
        rows = self.pand.shape[0]
        # None values to maintain the constistent rows length for each N
        nth_prior_measurements = [None]*N + [self.pand[feature][i-N] for i in range(N, rows)]
        col_name = "{}_{}".format(feature, N)
        self.pand[col_name] = nth_prior_measurements
        return

MLobject = ML('[49, 8]onlyRain.json')
MLobject.calculateLaggedInstance(3)
