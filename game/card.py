from constants import suits, ranks

class Card():
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def printCard(self):
		print(ranks[self.rank], 'of', suits[self.suit])
	
	