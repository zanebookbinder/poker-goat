from hand import Hand
import random

class Player():
	def __init__(self, name, index, chipCount):
		self.name = name
		self.index = index
		self.chipCount = chipCount
		self.debugOutput = False
		self.handWinCounter = 0
		self.startNewHand()

	def startNewHand(self):
		self.folded = False
		self.currentBet = 0
		self.hand = Hand()

	def bet(self, amount):
		self.currentBet += amount
		self.chipCount -= amount

	def takeTurn(self, options):
		action = None
		if options == ['preflop']:
			action = random.choice(['bet', 'check'])
			print("PREFLOP ACTION", action)
		if sorted(options) == ['call', 'fold']:
			action = 'call' if self.hasGoodHand() else 'fold'
		elif sorted(options) == ['bet', 'check']:
			action = 'bet' if self.hasGoodHand() else 'check'

		if self.debugOutput:
			print(self.name, 'takes action:', action)
		return action
	
	def hasGoodHand(self):
		handType, highCard, lowCard = self.hand.calculateSimpleHandValue()
		if handType == 'pair' or highCard > 7:
			return 'call'
		return 'fold'
	
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
	