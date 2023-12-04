from collections import defaultdict
from constants import REWARD_NORM
from handRankUtil import judgeHand, handTypeToValue, calculateSimpleHandValue
from handScoreUtil import scoreHand
class gameExperience():
	def __init__(self, round, bettingLevel, pot, holeCards, commonCards):
		self.round = round
		self.bettingLevel = bettingLevel
		self.pot = pot
		self.holeCards = None
		self.commonCards = None
		self.suitMode = None
		self.nextGameExperience = None
		self.reward = 0

		self.holeCardList = holeCards
		self.commonCardList = commonCards

		self.convertCardsIntoModelInput(holeCards, commonCards)

	def getAutoencoderInput(self):
		holeCardRepresentation = [0] * 52

		for holeCard in self.holeCardList:
			holeCardRepresentation[holeCard.suit * 13 + (holeCard.rank - 2)] = 1

		commonCardRepresentation = [0] * 52

		for commonCard in self.commonCardList:
			commonCardRepresentation[commonCard.suit * 13 + (commonCard.rank - 2)] = 1

		# 104 array of zeroes and ones
		return holeCardRepresentation + commonCardRepresentation
	
	def convertCardsIntoModelInput(self, holeCardObjects, commonCardObjects):
		
		playerHandCards = [0] * 13
		suitCounts = defaultdict(int)

		for card in holeCardObjects: #just use self.holeCards? doing this changed stuff in output so maybe not
			cardRank = card.rank
			playerHandCards[cardRank-2] += 1
			suitCounts[card.suit] += 1

		commonCards = [0] * 13
		for card in commonCardObjects:
			cardRank = card.rank
			commonCards[cardRank-2] += 1
			suitCounts[card.suit] += 1

		self.suitMode = max(suitCounts.values())
		self.holeCards = playerHandCards
		self.commonCards = commonCards

		# add hand rank score
		allCards = holeCardObjects + commonCardObjects

		if commonCardObjects:
			self.cardsScore = handTypeToValue[judgeHand(allCards)[0]] #2 card hand vs 5 card hand
		else:
			self.cardsScore = calculateSimpleHandValue(holeCardObjects)

		# normalize from 1-9 to -1 to 1
		self.cardsScore = ((self.cardsScore - 1) / 4) - 1

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
			# self.holeCards + \


		return [self.cardsScore]
	
		if self.commonCardList:
			handScore = scoreHand(self.holeCardList, self.commonCardList) * 2 - 1
		else:
			handScore = calculateSimpleHandValue(self.holeCardList)

		return [handScore] # -1 to 1

		# return \
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
