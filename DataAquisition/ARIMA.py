import os
from ML import *
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, median_absolute_error

class ARIMA:

    def __init__(self, dataName, lag):
        MLobject = ML(dataName)
        originalDataSeries = MLobject.calculateLaggedInstance(lag)
        X = originalDataSeries
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
        # instantiate the regressor class
        regressor = LinearRegression()

        # fit the build the model by fitting the regressor to the training data
        regressor.fit(X_train, y_train)

        # make a prediction set using the test set
        prediction = regressor.predict(X_test)
        return
