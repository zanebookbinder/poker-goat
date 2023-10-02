import player
from handScoreUtil import scoreHand
from keras.models import Sequential
from keras.models import Dense

class pokerPlayer(player):
    def __init__(self, model=None):
        if model:
            self.model = model
        else:
            model = self.createModel()
        

    def chooseAction(self, sharedCards, options):
        pass


    def createModel():
        model = Sequential()
        model.add(Dense(64, input_dim=27, activation= 'sigmoid'))
        model.add(Dense(14, activation = "relu"))
        model.add(Dense(8, activation = "relu"))
        model.add(Dense(3, activation  = "softmax"))

    def reward(holeCards, commonCards, action):
        probWin = scoreHand(holeCards, commonCards)
        if action == "fold":
            return 1 - 2 * probWin
        elif action == "check":
            pass
        elif action == "bet":
            return -1 + 2 * probWin
        elif action == "raise":
            pass



    


