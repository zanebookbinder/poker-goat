from utils import readExperiencesFile
from constants import REWARD_NORM
from model import Model
from card import Card

# horrible_cards = [
# 	[#1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 13 hole cards
# 		0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,  # 13 common cards
# 	2, 2, 3 / REWARD_NORM, 2 / REWARD_NORM, -1] # suit mode, round, betting level, pot amount, card score (normalized)
# ]

# four_aces = [
# 	[#0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  # 13 hole cards
# 		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,  # 13 common cards
# 	2, 2, 3 / REWARD_NORM, 2 / REWARD_NORM, 0.75] # suit mode, round, betting level, pot amount, card score (normalized)
# ]

# horrible_cards = [[-0.9]]
# four_aces = [[0.9]]



horrible_cards = [
	1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

four_aces = [
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, #HoleCards
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0	#CommonCards
]

def test_model(model, autoencoder):
	modelInput1 = autoencoder.predict([horrible_cards[:52]], verbose=0)[0]
	modelInput2 = autoencoder.predict([horrible_cards[52:]], verbose=0)[0]
	modelInput = modelInput1.tolist() + modelInput2.tolist()
	qVals = model.predict([modelInput],verbose=0)[0]
	print('With horrible cards:', qVals)

	modelInput1 = autoencoder.predict([four_aces[:52]], verbose=0)[0]
	modelInput2 = autoencoder.predict([four_aces[52:]], verbose=0)[0]
	modelInput = modelInput1.tolist() + modelInput2.tolist()
	qVals = model.predict([modelInput],verbose=0)[0]
	print('With four aces:', qVals)

import os
from keras.models import load_model, Model

model_dir = '/Users/zanebookbinder/Desktop/poker-goat/game/december_10th'
model_files = [f for f in os.listdir(model_dir) if f.endswith('.keras')]
model_files.sort(key = lambda x: int(x.replace('model_', '').replace('.keras', '')))

# Load the highest-verion model
largest_model_file = model_files[-1]
print(largest_model_file)

autoencoder_dir = '/Users/zanebookbinder/Desktop/poker-goat/game/autoencoder'
autoencoder_files = [f for f in os.listdir(autoencoder_dir) if f.endswith('.keras')]
autoencoder_files.sort(key = lambda x: int(x.replace('model_', '').replace('.keras', '')))
largest_ae_file = autoencoder_files[-1]


model = load_model(os.path.join(model_dir, largest_model_file))
autoencoder = load_model(os.path.join(autoencoder_dir, largest_ae_file))
autoencoder =  Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('dense_1').output)

test_model(model, autoencoder)








	   
	        
# test a specific input

# model = Model(load_model=True)
# qVals = model.model.predict(horrible_cards)
# print('with horrible cards:', qVals)
# qVals = model.model.predict(four_aces)
# print('with four aces:', qVals)
# # exit(0)

# print('\n\n\n')


# # get stats about experiences 
# experiences = readExperiencesFile()
# actionFreqs = [0,0,0]
# actionRewards = [0,0,0]

# wLByAction = [[0,0],[0,0],[0,0]]
# for e in experiences:
# 	state, action, nextState, reward = e
# 	actionFreqs[action] += 1
# 	actionRewards[action] += reward

# 	if reward > 0:
# 		wLByAction[action][0] += 1
# 	elif reward < 0:
# 		wLByAction[action][1] += 1

# print('Action frequencies:')
# print(actionFreqs)

# print('Action total rewards')
# print(actionRewards)

# print('WL by action')
# print(wLByAction)