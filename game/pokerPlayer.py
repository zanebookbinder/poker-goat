import player
from handScoreUtil import scoreHand
from keras.models import Sequential
from keras.models import Dense
import collections

class pokerPlayer(player):
    def __init__(self, model=None):
        self.model = model if model else self.createModel()

    def chooseAction(self, player, sharedCards, options):
        # TODO
        # Do a forward pass through the model (use getModelInput gameState function to get 28 inputs)
            # inputs are:
            #   1 for betting round (0 or 1)
            #   13 for hole card rank counts
            #   13 for common card rank counts
            #   1 for suit mode (across hole and common cards)
        # Find the reward (0 if first round of betting, net money change otherwise)
        # Train the model on that experience

        # should gameState be passed in here or something??
        modelInput = self.getModelInput(player, sharedCards)
        prediction = self.model.predict(modelInput)
        reward = self.reward(player.hand, sharedCards, prediction)

        # IS THIS THE RIGHT IDEA???
        loss = prediction - reward

        # I think this is the wrong function but idk
        self.model.train_on_batch(loss)
        return prediction

    def getModelInput(self, player, sharedCards):
        playerHandCards = [0] * 13
        suitCounts = collections.defaultdict(int)

        for card in player.hand.cards:
            cardRank = card.rank
            playerHandCards[cardRank-2] += 1
            suitCounts[card.suit] += 1

        commonCards = [0] * 13
        for card in sharedCards:
            cardRank = card.rank
            commonCards[cardRank-2] += 1
            suitCounts[card.suit] += 1

        suitMode = max(suitCounts.values())
        return [self.round] + playerHandCards + commonCards + [suitMode]

    def createModel():
        model = Sequential()
        model.add(Dense(64, input_dim=28, activation= 'sigmoid'))
        model.add(Dense(128, activation = "relu"))
        model.add(Dense(64, activation = "relu"))
        model.add(Dense(32, activation = "relu"))
        model.add(Dense(16, activation = "relu"))
        model.add(Dense(8, activation = "relu"))
        model.add(Dense(3, activation  = "softmax"))

    def reward(holeCards, commonCards, action):
        probWin = scoreHand(holeCards, commonCards)
        if action == "fold":
            return 1 - 2 * probWin
        elif action == "check":
            # why is this passing??
            pass
        elif action == "bet":
            return -1 + 2 * probWin
        elif action == "raise":
            pass



    


