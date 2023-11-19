from player import Player
from handScoreUtil import scoreHand

class SmartPlayer(Player):
	def __init__(self, name, index, chipCount):
		super().__init__(name, index, chipCount)

	def chooseBestAction(self, model, newGameExperience, commonCards):
		handScore = scoreHand(self.hand.cards, commonCards)

		if handScore > 0.7:
			return 2
		
		if handScore > 0.4:
			return 1
		
		return 0

