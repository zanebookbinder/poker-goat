import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from utils import readExperiencesFile
import tensorflow as tf

class Model():
    def __init__(self, model=None):
        if not model:
            self.createModel()
        else:
            self.model = model

    def chooseBestAction(self, gameExperience):
        modelInput = np.array(gameExperience.getState()).reshape(1, -1)
        
        bestAction = self.model.predict(modelInput)
        # returns [x, y, z] where:
        # x + y + z = 1
        # x --> check/fold
        # y --> bet
        # z --> raise
    
        return int(np.argmax(bestAction))

    def createModel(self):
        model = Sequential()
        model.add(Dense(64, input_dim=30, activation= 'sigmoid'))
        model.add(Dense(128, activation = "relu"))
        model.add(Dense(64, activation = "relu"))
        model.add(Dense(32, activation = "relu"))
        model.add(Dense(16, activation = "relu"))
        model.add(Dense(8, activation = "relu"))
        model.add(Dense(3, activation  = "softmax"))
        model.compile(loss="mse", optimizer="Adam")
        self.model = model

    def saveModel(self):
        self.model.save("playerModel.keras")

    def trainModel(self):
        experiences = readExperiencesFile()

        # with replacement???
        sample_size = 10
        samples = [random.choice(experiences) for _ in range(sample_size)]

        x = np.empty((sample_size, 30))
        YTarget = np.empty((sample_size, 3))
        for i, sample in enumerate(samples):
            state, action, nextState, reward = sample
            x[i] = np.array(state)
            state2D = np.array(state).reshape(1, -1)
            if not nextState:
                Qmax = 0
            else:
                nextState = np.array(nextState).reshape(1, -1)
                QPrimeOutput = self.model.predict(nextState)[0]
                Qmax = max(QPrimeOutput)
            
            prediction = self.model.predict(state2D)[0]
            y_actual = prediction.copy()
            y_actual[action] = Qmax + reward
            
            YTarget[i] = y_actual

        print(x)
        print('----')
        print(YTarget)

        self.model.fit(x, YTarget)            