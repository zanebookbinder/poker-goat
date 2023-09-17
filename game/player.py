from hand import Hand
import random

class Player():
	def __init__(self, name, index, chipCount):
		self.name = name
		self.index = index
		self.hand = Hand()
		self.currentBet = 0
		self.chipCount = chipCount
		self.folded = False
		self.debugOutput = True

	def bet(self, amount):
		self.currentBet += amount
		self.chipCount -= amount

	def takeTurn(self, options):
		result = random.choice(options)
		if self.debugOutput:
			print(self.name, 'takes action:', result)
		return result
	
	def receiveCard(self, card):
		self.hand.addCardToHand(card)

	def printPlayerInfo(self):
		print(self.name, 'has:')
		for card in self.hand.cards:
			card.printCard()
		print('Current Chip count: ', str(int(self.chipCount)))
		if self.folded:
			print('** Has already folded **')
		print('')
	