from deck import Deck
from constants import dealSystem, commonCardSize
from handRankUtil import *

"""
The state of a Poker Game, including bets, cards, players, etc.
"""
class GameState():
	def __init__(self, players, start_ante):
		self.players = players
		self.ante = start_ante

	def startNewHand(self):
		self.startingChipAmounts = [player.chipCount for player in self.players]
		self.sharedCards = []
		self.pot = 0
		for player in self.players:
			player.startNewHand()
			player.chipCount -= self.ante
			self.pot += self.ante

		self.turn = 0
		self.round = 0
		self.deck = Deck()
		self.deal()
		
		#currentRoundBet notes how much each player must have in the pot in order to continue playing
		self.currentRoundBet = 0
		self.winner = None

	def startNewRound(self):
		self.round += 1
		self.currentRoundBet = 0
		for player in self.players:
			player.currentBet = 0
		
	def deal(self):
		numCardsToDeal = dealSystem[self.round]
		for _ in range(numCardsToDeal):
			for i in range(len(self.players)):
				nextCard = self.deck.selectRandomCard()
				self.players[i].receiveCard(nextCard)

		numCardsToDeal = commonCardSize
		for _ in range(numCardsToDeal):
			nextCard = self.deck.selectRandomCard()
			self.sharedCards.append(nextCard)

	def bet(self, playerIndex, amount):
		self.players[playerIndex].bet(amount)
		self.pot += amount
		self.currentRoundBet = max(self.currentRoundBet, self.players[playerIndex].currentBet)

	def fold(self, playerIndex):
		self.players[playerIndex].folded = True
		self.players[playerIndex].foldedCounter += 1

	def getActivePlayers(self):
		return [p for p in self.players if not p.folded]

	def checkWinner(self):
		activePlayers = self.getActivePlayers()
		if len(activePlayers) == 1:
			self.winner = activePlayers[0]
			self.winner.chipCount += self.pot
			self.winner.handWinCounter += 1
			self.winnerDict = {self.winner: 'wins as the only remaining player'}
			return self.winnerDict
		
		playerHands = [p.hand.cards + self.sharedCards for p in activePlayers]
		winningPlayersIndicesToHandsDict = compareAllHands(playerHands)
		# looks something like this: {0: ('junk', [14, 11, 7, 6, 5])}
		
		winningPlayersToHandsDict = {self.players[key]: value for key, value in winningPlayersIndicesToHandsDict.items()}
		
		for p in winningPlayersToHandsDict.keys():
			p.chipCount += self.pot / len(winningPlayersToHandsDict.keys())
			p.handWinCounter += 1

		self.winnerDict = winningPlayersToHandsDict
		return self.winnerDict

	def summarizeGame(self):
		for p in self.players:
			print(p.name, 'won', p.handWinCounter, 'hands and folded', p.foldedCounter, 'times')
		print('')

		for player in self.players:
			player.printPlayerInfo()

		print('Shared cards:')
		for card in self.sharedCards:
			card.printCard()
		print('')

		for winningPlayer, hand in self.winnerDict.items():
			if type(hand) == str: # all players folded, one player left
				print(winningPlayer.name, 'wins as the only remaining player')
			else:
				print(winningPlayer.name, 'wins with', hand[0])
		# print('Winning player(s):', ', '.join(winners))
