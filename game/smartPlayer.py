from player import Player
from handScoreUtil import scoreHand
import numpy as np
from handRankUtil import calculateSimpleHandValue

"""
A Player subclass that chooses actions based on hand strength.
"""
class SmartPlayer(Player):
	def __init__(self, name, index, chipCount):
		super().__init__(name, index, chipCount)

	def chooseBestAction(self, model, newGameExperience, commonCards):
		if commonCards:
			handScore = scoreHand(self.hand.cards, commonCards)
		else:
			handScore = calculateSimpleHandValue(self.hand.cards)
			handScore = (handScore + 1) / 2

		actions = [0, 1, 2]

		if handScore > 0.6:
			probs = [0, 0.4, 0.6]
		elif handScore > 0.3:
			probs = [0.2, 0.6, 0.2]
		else:
			probs = [0.7, 0.2, 0.1]

		return np.random.choice(
			actions,
			p = probs
		)

