from card import Card

class Hand():
	def __init__(self):
		self.cards = []

	def addCardToHand(self, card):
		self.cards.append(card)

	def calculateHandValue(self):
		return sum([card.rank for card in self.cards])

	
	