from collections import defaultdict
from constants import REWARD_NORM
	
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

		self.convertCardsIntoModelInput(holeCards, commonCards)
	
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

	def setNextGameExperience(self, nextGameExperience):
		self.nextGameExperience = nextGameExperience

	def setGameReward(self, reward):
		self.reward = reward / REWARD_NORM

	def setActionTaken(self, action):
		self.action = action

	def getState(self):
		return \
			self.holeCards + \
			self.commonCards + \
			[
				self.suitMode, 
				self.round,
				self.bettingLevel / ,
				self.pot / REWARD_NORM,
			]

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
