from constants import REWARD_NORM
from handRankUtil import calculateSimpleHandValue
from handScoreUtil import scoreHand

"""
A class that represents an (s,a,s',r) state as a GameExperience.
"""

class gameExperience():
	def __init__(self, round, bettingLevel, pot, holeCards, commonCards, autoencoder):
		self.round = round
		self.bettingLevel = bettingLevel
		self.pot = pot
		self.holeCards = None
		self.commonCards = None
		self.suitMode = None
		self.nextGameExperience = None
		self.reward = 0
		self.autoencoder = autoencoder

		self.holeCardList = holeCards
		self.commonCardList = commonCards

		self.convertCardsIntoModelInput(holeCards, commonCards)
	
	def getAutoencoderInput(self, cardList):
		output = [0] * 52

		for card in cardList:
			output[(card.rank - 2) * 4 + card.suit] = 1

		# 52-length array of zeroes and ones
		return output
	
	def convertCardsIntoModelInput(self, holeCardObjects, commonCardObjects):
		modelInput1 = self.autoencoder.predict([self.getAutoencoderInput(holeCardObjects)], verbose=0)[0]
		modelInput2 = self.autoencoder.predict([self.getAutoencoderInput(commonCardObjects)], verbose=0)[0]

		self.modelInput = modelInput1.tolist() +  modelInput2.tolist()

		# print(modelInput1 + modelInput2)
		# print(len(self.modelInput), self.modelInput)
		# playerHandCards = [0] * 13
		# suitCounts = defaultdict(int)

		# for card in holeCardObjects: #just use self.holeCards? doing this changed stuff in output so maybe not
		# 	cardRank = card.rank
		# 	playerHandCards[cardRank-2] += 1
		# 	suitCounts[card.suit] += 1

		# commonCards = [0] * 13
		# for card in commonCardObjects:
		# 	cardRank = card.rank
		# 	commonCards[cardRank-2] += 1
		# 	suitCounts[card.suit] += 1

		# self.suitMode = max(suitCounts.values())
		# self.holeCards = playerHandCards
		# self.commonCards = commonCards

		# # add hand rank score
		# allCards = holeCardObjects + commonCardObjects

		# if commonCardObjects:
		# 	self.cardsScore = handTypeToValue[judgeHand(allCards)[0]]

		# 	# normalize from 1-9 to -1 to 1
		# 	self.cardsScore = ((self.cardsScore - 1) / 4) - 1
		# else:
		# 	# don't need to normalize, already in [-1, 1]
		# 	self.cardsScore = calculateSimpleHandValue(holeCardObjects)

	def setNextGameExperience(self, nextGameExperience):
		self.nextGameExperience = nextGameExperience

	def setGameReward(self, reward):
		# risk-averse player
		# if reward < 0:
		# 	reward *= 1.5
			
		self.reward = reward / REWARD_NORM

	def setActionTaken(self, action):
		self.action = action

	def getState(self):
		
		# output from autoencoder (16-length)
		return [self.modelInput]
	
		# hand score model input idea (somewhat worked?)
		# if self.commonCardList:
		# 	handScore = scoreHand(self.holeCardList, self.commonCardList) * 2 - 1
		# else:
		# 	handScore = calculateSimpleHandValue(self.holeCardList)

		# return [handScore] # -1 to 1

		# our original model input idea (didn't work)
		# return \
		# 	self.holeCards + \
		# 	self.commonCards + \
		# 	[
		# 		self.suitMode, 
		# 		self.round,
		# 		self.bettingLevel / REWARD_NORM,
		# 		self.pot / REWARD_NORM,
		# 		self.cardsScore
		# 	]

	def getRLInfo(self):
		nextState = self.nextGameExperience.getState() if self.nextGameExperience else []
		
		return [
			self.getState(),
			self.action,
			nextState,
			self.reward
		]

	def summarizeGameExperience(self):
		print(self.getRLInfo())
