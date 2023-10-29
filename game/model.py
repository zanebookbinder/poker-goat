import numpy as np
from sklearn import preprocessing
import random
from keras.models import Sequential
from keras.layers import Dense
from utils import readExperiencesFile

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

    # def getModelInput(self, player, sharedCards):
    #     playerHandCards = [0] * 13
    #     suitCounts = collections.defaultdict(int)

    #     for card in player.hand.cards:
    #         cardRank = card.rank
    #         playerHandCards[cardRank-2] += 1
    #         suitCounts[card.suit] += 1

    #     commonCards = [0] * 13
    #     for card in sharedCards:
    #         cardRank = card.rank
    #         commonCards[cardRank-2] += 1
    #         suitCounts[card.suit] += 1

    #     suitMode = max(suitCounts.values())
    #     return [self.round] + playerHandCards + commonCards + [suitMode]

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
        samples = [random.choice(experiences) for _ in range(10)]
        
        X = []
        YTarget = []
        for sample in samples:
            state, action, nextState, reward = sample
            state = np.array(state).reshape(1, -1)
            X.append(state)
            if not nextState:
                Qmax = 0
            else:
                nextState = np.array(nextState).reshape(1, -1)
                QPrimeOutput = self.model.predict(nextState)[0]
                Qmax = max(QPrimeOutput)
            
            prediction = self.model.predict(state)[0]
            y_actual = prediction.copy()

            y_actual[action] = Qmax + reward #normalize this??
            y_actual = preprocessing.normalize([y_actual])
            YTarget.append(np.array(y_actual).reshape(1, -1)) 

        print(X)
        print('----')
        print(YTarget)

        # self.model.fit(X, YTarget)
        self.model.train_on_batch(X, YTarget)
            
            