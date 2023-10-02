from constants import suits, ranks

class Card():
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def sameCard(self, card):
		return self.suit == card.suit and self.rank == card.rank

	def printCard(self):
		print(ranks[self.rank], 'of', suits[self.suit])
	
	