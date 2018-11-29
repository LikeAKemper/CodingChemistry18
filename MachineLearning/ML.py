import os
import pandas as pd




class ML:

    def __init__(self, fileName):
        os.chdir('../DataAquisition/JsonFiles')
        f = open(fileName, 'r')
        str = f.read()
        os.chdir('../../MachineLearning')
        self.pand = pd.read_json(str)
        return

    def calculateLaggedInstance(self, lag):
        """
        for each day (row) and for a given feature (column) add value for that feature N days
        prior
        For each value of N (1-3 in our case) a new column is added for that feature representing
        the Nth prior day's measurement.
        """
        # 1 day prior
        N = 1

ML = ML('[49, 8].pand.json')
