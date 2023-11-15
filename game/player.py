from hand import Hand
import random
from handRankUtil import judgeHand
from handScoreUtil import scoreHand

class Player():
	def __init__(self, name, index, chipCount):
		self.name = name
		self.index = index
		self.chipCount = chipCount
		self.debugOutput = False
		self.handWinCounter = 0
		self.foldedCounter = 0
		self.hasTakenATurnThisHand = False
		self.startNewHand()

	def startNewHand(self):
		self.folded = False
		self.currentBet = 0
		self.hand = Hand()
		self.hasTakenATurnThisHand  = False

	def bet(self, amount):
		self.currentBet += amount
		self.chipCount -= amount

	def hasGoodHoleCards(self):
		handType, highCard, lowCard = self.hand.calculateSimpleHandValue()
		if handType == 'pair' or highCard > 11:
			return 2
		
		if highCard > 7:
			return 1

		if highCard - lowCard == 1 and lowCard > 3 and random.random() > 0.5:
			return 1
		
		if self.hand.suitedHand() and random.random() > 0.5:
			return 1
		
		return 0
	
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
	