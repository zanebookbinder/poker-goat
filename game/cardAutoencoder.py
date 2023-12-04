import numpy as np
import random
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Input
import os
from utils import readExperiencesFile, expToFile, deleteFileContent
from constants import BATCH_SIZE, STARTING_EPSILON, EPSILON_MULTIPLIER
from deck import Deck


class AutoEncoder():
    def __init__(self, load_model = True, common = False):
        self.common = common
            
        if load_model:
            self.model, iteration = self.loadModelFromFile()
            self.model_iteration = iteration
        else:
            self.model_iteration = 0
            self.createModel()

        for i in range(100):
            print(i)
            data = self.generateShitTonOfHands()
            self.trainModel(data)

    def generateShitTonOfHands(self):
        outputHands = []

        for _ in range(10000):
            deck = Deck()
            holeCards = []
            commonCards = []

            for _ in range(2):
                nextCard = deck.selectRandomCard()
                holeCards.append(nextCard)

            if not self.common:    
                outputHands.append(self.getAutoencoderInput(holeCards, commonCards))
                continue

            for _ in range(3):
                commonCards.append(deck.selectRandomCard())

            outputHands.append(self.getAutoencoderInput(holeCards, commonCards))

        return outputHands

    def getAutoencoderInput(self, holeCardList, commonCardList):
        holeCardRepresentation = [0] * 52

        for holeCard in holeCardList:
            holeCardRepresentation[holeCard.suit * 13 + (holeCard.rank - 2)] = 1

        commonCardRepresentation = [0] * 52

        for commonCard in commonCardList:
            commonCardRepresentation[commonCard.suit * 13 + (commonCard.rank - 2)] = 1

        # 104 array of zeroes and ones
        return holeCardRepresentation + commonCardRepresentation

    def createModel(self):
        input_data = Input(shape=(104,))

        encoded = Dense(64, activation='relu')(input_data)
        encoded = Dense(32, activation='relu')(encoded)
        encoded = Dense(10, activation='relu')(encoded)  # Encoding into 10 dimensions

        decoded = Dense(32, activation='relu')(encoded)
        decoded = Dense(64, activation='relu')(decoded)
        decoded = Dense(104, activation='sigmoid')(decoded)  # Output layer with sigmoid activation

        autoencoder = Model(input_data, decoded)
        autoencoder.compile(optimizer='adam', loss='binary_crossentropy')  # Adjust loss based on your problem
        self.model = autoencoder

    def trainModel(self, experiences):
        self.model.fit(experiences, experiences)

        input = [
            1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ]
        if self.common:
            input = [
            1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1
        ]
            
        result = self.model.predict([input])[0]
        
        loss = sum([abs(input[i] - result[i]) for i in range(104)])

        if not self.model_iteration % 5:
            print(result)
            
        print(loss)
        if self.common:
            status = "common"
        else:
            status = "hole"
        self.saveModel(file_name='autoencoder/' + status + '_model_' + str(self.model_iteration) + '.keras')
        self.model_iteration += 1  

    def saveModel(self, file_name = "model.keras"):
        self.model.save(file_name)

    def loadModelFromFile(self):
        model_dir = './autoencoder'
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.keras')]
        model_files.sort(key = lambda x: int(x.replace('model_', '').replace('.keras', '')))

        if model_files:
            # Load the highest-verion model
            largest_model_file = model_files[-1]
            return load_model(os.path.join(model_dir, largest_model_file)), int(largest_model_file.replace('model_', '').replace('.keras', ''))
        else:
            print("No model files found in the directory")

    def extractDenseFeatures(self, data):
        encoder = Model(inputs=self.model.input, outputs=self.model.get_layer('dense_3').output)
        encoded_data = encoder.predict(data)
        return encoded_data #Return an array of size 10 with representative information of 104 cards

AutoEncoder(load_model = False, common = False)
AutoEncoder(load_model = False, common = True)