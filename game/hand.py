from card import Card

class Hand():
	def __init__(self):
		self.cards = []

	def addCardToHand(self, card):
		self.cards.append(card)

	def suitedHand(self):
		return len(set([card.suit for card in self.cards])) == 1

	def calculateSimpleHandValue(self):
		if self.cards[0].rank == self.cards[1].rank:
			return ('pair', self.cards[0].rank, self.cards[1].rank)

		return ('junk', max([c.rank for c in self.cards]), min([c.rank for c in self.cards]))

	
	