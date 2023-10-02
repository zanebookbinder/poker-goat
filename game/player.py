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
		self.startNewHand()

	def startNewHand(self):
		self.folded = False
		self.currentBet = 0
		self.hand = Hand()

	def bet(self, amount):
		self.currentBet += amount
		print('PLAYER CURRENT BET IS NOW', self.currentBet)
		self.chipCount -= amount

	def chooseAction(self, sharedCards, options):
		action = None
		if not sharedCards:
			print('Good hole cards --> bet' if self.hasGoodHoleCards() else 'Bad hole cards --> check/fold')
			if options == ['bet', 'fold']:
				action = 'bet' if self.hasGoodHoleCards() else 'fold'
			elif options == ['bet', 'check']:
				action = 'bet' if self.hasGoodHoleCards() else 'check'
			else:
				print("ALERT", options)
		else:
			score = scoreHand(self.hand.cards, sharedCards)
			print('Good 5-card hand --> bet' if score > 0.5 else 'Bad 5-card hand --> check/fold')

			if options == ['bet', 'fold']:
				action = 'bet' if score > 0.5 else 'fold'
			elif options == ['bet', 'check']:
				action = 'bet' if score > 0.5 else 'check'

		if self.debugOutput:
			print(self.name, 'takes action:', action)
		return action
	
	def hasGoodHoleCards(self):
		handType, highCard, lowCard = self.hand.calculateSimpleHandValue()
		if handType == 'pair' or highCard > 7:
			return True
		
		return False
	
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
	