import numpy as np
import random
from keras.models import Sequential, load_model
from keras.models import Model as KerasModel
from keras.layers import Dense
import os
from utils import readExperiencesFile, expToFile, deleteFileContent
from constants import BATCH_SIZE, STARTING_EPSILON, EPSILON_MULTIPLIER, MODEL_INPUT_SIZE

"""
A deep Q network that trains on game experiences, use MSE loss, where the loss 
is the different between the correct Q value and the predicted Q value.
"""
class Model():
    def __init__(self, load_model=False):
        if load_model:
            self.model = self.loadModelFromFile()
        else:
            self.createModel()
            deleteFileContent()

        self.model_iteration = 0
        self.epsilon = STARTING_EPSILON
        self.autoencoder = self.loadAutoencoder()

    # load the most-trained autoencoder from the /autoencoder directory
    def loadAutoencoder(self):
        model_dir = './autoencoder'
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.keras')]
        model_files.sort(key = lambda x: int(x.replace('model_', '').replace('.keras', '')))

        if model_files:
            largest_model_file = model_files[-1]
            autoencoder = load_model(os.path.join(model_dir, largest_model_file))
            return KerasModel(inputs=autoencoder.input, outputs=autoencoder.get_layer('dense_1').output)
        else:
            print("No model files found in the directory")

    # use the model to determine the optimal action, given a GameExperience
    def chooseBestAction(self, gameExperience):
        # random action with probability EPSILON
        if random.random() < self.epsilon:
            return random.choice([0,1,2])

        modelInput1 = self.autoencoder.predict([gameExperience.getAutoencoderInput(gameExperience.holeCardList)], verbose=0)[0]
        modelInput2 = self.autoencoder.predict([gameExperience.getAutoencoderInput(gameExperience.commonCardList)], verbose=0)[0]

        modelInput = [modelInput1.tolist() +  modelInput2.tolist()]
        
        # fetches three Q values: [check/fold, bet/call, raise]
        bestAction = self.model.predict(modelInput, verbose=0)[0]

        return int(np.argmax(bestAction)) # choose the best one

    # create the network structure
    def createModel(self):
        model = Sequential()
        model.add(Dense(16, input_dim=MODEL_INPUT_SIZE, activation= 'sigmoid'))
        model.add(Dense(8, activation = "relu"))
        model.add(Dense(3, activation  = "linear"))
        # model.add(Dense(64, input_dim=18, activation= 'sigmoid'))
        # model.add(Dense(128, activation = "relu"))
        # model.add(Dense(64, activation = "relu"))
        # model.add(Dense(32, activation = "relu"))
        # model.add(Dense(16, activation = "relu"))
        # model.add(Dense(8, activation = "relu"))
        # model.add(Dense(3, activation  = "linear"))
        model.compile(loss="mse", optimizer="Adam")
        self.model = model

    def saveModel(self, file_name = "model.keras"):
        self.model.save(file_name)

    def loadModelFromFile(self):
        model_dir = './models'
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.keras')]
        model_files.sort(key = lambda x: int(x.replace('model_', '').replace('.keras', '')))

        if model_files:
            largest_model_file = model_files[-1]
            return load_model(os.path.join(model_dir, largest_model_file))
        else:
            print("No model files found in the directory")

    def trainModel(self):
        experiences = readExperiencesFile()

        # sample without replacement
        sample_size = int(BATCH_SIZE / 2)
        samples = random.sample(experiences, sample_size)

        new_experiences = [e for e in experiences if e not in samples]
        expToFile(new_experiences)

        # create the YTarget array usting the Q update equation (Bellman?)
        x = np.empty((sample_size, MODEL_INPUT_SIZE))
        YTarget = np.empty((sample_size, 3))
        for i, sample in enumerate(samples):
            state, action, nextState, reward = sample
            x[i] = np.array(state)
            state2D = np.array(state).reshape(1, -1)
            if not nextState:
                Qmax = 0
            else:
                nextState = np.array(nextState).reshape(1, -1)
                QPrimeOutput = self.model.predict(nextState, verbose=0)[0]
                Qmax = max(QPrimeOutput)
            
            prediction = self.model.predict(state2D, verbose=0)[0]
            y_actual = prediction.copy()
            y_actual[action] = Qmax + reward
            
            YTarget[i] = y_actual

        self.model.fit(x, YTarget, verbose=0) 

        if not self.model_iteration % 10:
            self.saveModel(file_name='december_10th/model_' + str(self.model_iteration) + '.keras')
            # from model_tester import test_model
            # test_model(self.model)  
        self.model_iteration += 1     
        self.epsilon *= EPSILON_MULTIPLIER

