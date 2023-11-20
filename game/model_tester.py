from utils import readExperiencesFile
from constants import REWARD_NORM
from model import Model

horrible_cards = [
	[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 13 hole cards
		0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,  # 13 common cards
	2, 2, 3 / REWARD_NORM, 2 / REWARD_NORM] # suit mode, round, betting level, pot amount
]

four_aces = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  # 13 hole cards
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,  # 13 common cards
	2, 2, 4 / REWARD_NORM, 6 / REWARD_NORM] # suit mode, round, betting level, pot amount
]

def test_model(model):
	qVals = model.predict(horrible_cards)
	print('with horrible cards:', qVals)
	qVals = model.predict(four_aces)
	print('with four aces:', qVals)
            
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