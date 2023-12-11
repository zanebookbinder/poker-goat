import numpy as np
import random
from keras.models import  Model, load_model
from keras.layers import Dense, Input
import os


class AutoEncoder():
    def __init__(self, load_model = True):
        if load_model:
            self.model, iteration = self.loadModelFromFile()
            self.model_iteration = iteration
        else:
            self.model_iteration = 0
            self.createModel()

        print('Generating all hands...')
        data = self.generateAllHands()
        print('Done generating all hands, traning now...')
        for i in range(1000):
            if not i % 10:
                print('Epoch:', i)
            
            self.trainModel(data)

        print('Finished training!')

    def generateAllHands(self):
        outputHands = []

        for card1 in range(52):
            for card2 in range(card1 + 1, 52):
                newArr = [1 if i in [card1, card2] else 0 for i in range(52)]
                outputHands.append(newArr)

                for card3 in range(card2 + 1, 52):
                    newNewArr = newArr[:]
                    newNewArr[card3] = 1
                    outputHands.append(newNewArr)

        return outputHands

        # for _ in range(10000):
        #     deck = Deck()
        #     holeCards = []
        #     commonCards = []

        #     for _ in range(2):
        #         nextCard = deck.selectRandomCard()
        #         holeCards.append(nextCard)

        #     if not self.common:    
        #         outputHands.append(self.getAutoencoderInput(holeCards, commonCards))
        #         continue

        #     for _ in range(3):
        #         commonCards.append(deck.selectRandomCard())

        #     outputHands.append(self.getAutoencoderInput(holeCards, commonCards))

    def getAutoencoderInput(self, cardList):
        output = [0] * 52

        for card in cardList:
            output[(card.rank - 2) * 4 + card.suit] = 1

        # 52-length array of zeroes and ones
        return output

    def createModel(self):
        input_data = Input(shape=(52,))

        encoded = Dense(16, activation='relu')(input_data)
        # encoded = Dense(32, activation='relu')(encoded)
        encoded = Dense(8, activation='relu')(encoded)  # Encoding into 10 dimensions

        decoded = Dense(16, activation='relu')(encoded)
        # decoded = Dense(64, activation='relu')(decoded)
        decoded = Dense(52, activation='sigmoid')(decoded)  # Output layer with sigmoid activation

        autoencoder = Model(input_data, decoded)
        autoencoder.compile(optimizer='adam', loss='binary_crossentropy')  # Adjust loss based on your problem
        self.model = autoencoder

    def trainModel(self, experiences):
        self.model.fit(experiences, experiences, verbose=0)
        
        if not self.model_iteration % 50:
            input = [
                1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ]
            result = self.model.predict([input], verbose=0)[0]
            loss = sum([abs(input[i] - result[i]) for i in range(52)])
            print('One test loss:', loss)
            print(result)

        inputs = []
        for _ in range(10):
            random_numbers = [random.randint(0, 51) for _ in range(3)]
            input = [0] * 52
            for num in random_numbers:
                input[num] = 1
            inputs.append(input)
            
        result = self.model.predict(inputs, verbose=0)
        total_loss = 0
        for j in range(len(result)):
            total_loss += sum([abs(inputs[j][i] - result[j][i]) for i in range(52)]) 
        
        print('Total loss', total_loss)
        
        if not self.model_iteration % 50:
            self.saveModel(file_name='autoencoder/model_' + str(self.model_iteration) + '.keras')
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


AutoEncoder(load_model = False)