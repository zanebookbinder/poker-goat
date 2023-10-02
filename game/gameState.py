from deck import Deck
from constants import dealSystem, commonCardSize
from player import Player
from handRankUtil import *

class GameState():
	def __init__(self, players, start_ante):
		self.players = players
		self.ante = start_ante

	def startNewHand(self):
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
		self.currentRoundBet = max(self.currentRoundBet, amount)

	def fold(self, playerIndex):
		self.players[playerIndex].folded = True
		activePlayers = self.getActivePlayers()
		if len(activePlayers) == 1:
			self.winner = activePlayers[0]

	def getActivePlayers(self):
		return [p for p in self.players if not p.folded]

	def checkWinner(self):
		if self.winner:
			self.winner.chipCount += self.pot
			self.winner.handWinCounter += 1
			self.winnerDict = {self.winner: 'wins as the only remaining player'}
			return self.winnerDict
		
		playerHands = [p.hand.cards + self.sharedCards for p in self.players]
		winningPlayersIndicesToHandsDict = compareAllHands(playerHands)
		# looks something like this: {0: ('junk', [14, 11, 7, 6, 5])}
		
		winningPlayersToHandsDict = {self.players[key]: value for key, value in winningPlayersIndicesToHandsDict.items()}
		
		for p in winningPlayersToHandsDict.keys():
			p.chipCount += self.pot / len(winningPlayersToHandsDict.keys())
			p.handWinCounter += 1

		self.winnerDict = winningPlayersToHandsDict
		return self.winnerDict

	def summarizeGame(self):
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
	
	