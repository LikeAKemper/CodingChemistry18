from kNN import *


class compareMachine:

    def __init__(self, nameOfDataSet):
        lag = 10
        nNeighbors = 5
        NNR = kNN(nameOfDataSet, lag, nNeighbors)
        pass
