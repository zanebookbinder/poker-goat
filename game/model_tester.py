from model import Model
from utils import readExperiencesFile

horrible_cards = [
	[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 13 hole cards
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 13 common cards
	2, 1, 0, 2] # suit mode, round, betting level, pot amount
]

four_aces = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  # 13 hole cards
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,  # 13 common cards
	2, 2, 4, 6] # suit mode, round, betting level, pot amount
]
            
# test a specific input
model = Model(load_model=True)
qVals = model.model.predict(four_aces)
print(qVals)

# get stats about experiences 
experiences = readExperiencesFile()
actionFreqs = [0,0,0]
actionRewards = [0,0,0]

wLByAction = [[0,0],[0,0],[0,0]]
for e in experiences:
	state, action, nextState, reward = e
	actionFreqs[action] += 1
	actionRewards[action] += reward

	if reward > 0:
		wLByAction[action][0] += 1
	elif reward < 0:
		wLByAction[action][1] += 1

print(actionFreqs)
print(actionRewards)
print(wLByAction)