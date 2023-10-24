
	
class gameExperience():
	def __init__(self, round, bettingLevel, pot, holeCards, commonCards):
		self.round = round
		self.bettingLevel = bettingLevel
		self.pot = pot
		self.holeCards = None
		self.commonCards = None
		self.suitMode = None
		self.nextGameState = None

		self.convertCardsIntoModelInput(holeCards, commonCards)
	
	def convertCardsIntoModelInput(self, holeCardObjects, commonCardObjects):
        playerHandCards = [0] * 13
        suitCounts = collections.defaultdict(int)

        for card in holeCardObjects:
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

	def addNextGameState(self, nextGameState):
		self.nextGameState = nextGameState

	def setGameReward(self, reward):
		self.reward = reward

	def setActionTaken(self, action):
		self.action = action

	def getRLInfo(self):
		return (
			self.holeCards + \
			self.commonCards + \
			[
				self.suitMode, 
				self.round,
				self.bettingLevel,
				self.pot,
			],
			self.action,
			self.nextGameState,
			self.reward
		)