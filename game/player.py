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
		self.startNewHand()

	def startNewHand(self):
		self.folded = False
		self.currentBet = 0
		self.hand = Hand()

	def bet(self, amount):
		self.currentBet += amount
		self.chipCount -= amount

	def chooseAction(self, sharedCards, options):
		action = None
		if not sharedCards:
			holeCardRating = self.hasGoodHoleCards()
			if self.debugOutput:
				prints = ['Great hole cards --> raise', 'Good hole cards --> bet', 'Bad hole cards --> check/fold']
				print(prints[holeCardRating])
			if options == ['bet', 'fold', 'raise']:
				if holeCardRating == 2:
					action = 'raise'
				elif holeCardRating == 1:
					action = 'bet'
				else:
					action = 'fold'
			elif options == ['bet', 'check', 'raise']:
				if holeCardRating == 2:
					action = 'raise'
				elif holeCardRating == 1:
					action = 'bet'
				else:
					action = 'check'
			else:
				print("ALERT, THESE OPTIONS ARE NOT OK", options)
		else:
			score = scoreHand(self.hand.cards, sharedCards)
			scoreRating = 0
			if score > 0.75:
				scoreRating = 2
			elif score > 0.5:
				scoreRating = 1

			if self.debugOutput:
				prints = ['Great 5-card hand --> raise', 'Good 5-card hand --> bet', 'Bad 5-card hand --> check/fold']
				print(prints[scoreRating])

			if options == ['bet', 'fold', 'raise']:
				action = ['fold', 'bet', 'raise'][scoreRating]
			elif options == ['bet', 'check', 'raise']:
				action = ['check', 'bet', 'raise'][scoreRating]
			else:
				print("ALERT, THESE OPTIONS ARE NOT OK", options)

		if self.debugOutput:
			print(self.name, 'takes action:', action)
		return action
	
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
	