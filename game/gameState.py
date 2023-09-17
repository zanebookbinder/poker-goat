from deck import Deck
from constants import dealSystem
from player import Player

class GameState():
	def __init__(self, players, start_ante):
		self.players = players
		self.ante = start_ante
		self.startNewHand()

	def startNewHand(self):
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
		

	def deal(self):
		numCardsToDeal = dealSystem[self.round]
		for _ in range(numCardsToDeal):
			for i in range(len(self.players)):
				nextCard = self.deck.selectRandomCard()
				self.players[i].receiveCard(nextCard)

	def bet(self, playerIndex, amount):
		self.players[playerIndex].bet(amount)
		self.pot += amount
		self.currentRoundBet = max(self.currentRoundBet, self.players[playerIndex].currentBet)

	def call(self, playerIndex):
		self.bet(playerIndex, self.currentRoundBet)

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
			return [self.winner.name]
		
		activePlayers = self.getActivePlayers()
		bestHand = ['junk', -1, -1]
		winning = []
		for p in activePlayers:
			handType, bestCard, worstCard = p.hand.calculateSimpleHandValue()
			if bestHand[0] == 'junk' and handType == 'pair':
				bestHand = ['pair', bestCard, worstCard]
				winning = [p]

			elif bestHand[0] == 'junk' and handType == 'junk':
				if bestCard > bestHand[1]:
					bestHand = ['junk', bestCard, worstCard]
					winning = [p]
				elif bestCard == bestHand[1]:
					if worstCard > bestHand[2]:
						bestHand = ['junk', bestCard, worstCard]
						winning = [p]
					elif worstCard == bestHand[2]:
						winning.append(p)

			
			elif bestHand[0] == 'pair' and handType == 'pair':
				if bestCard > bestHand[1]:
					bestHand = ['pair', bestCard, worstCard]
					winning = [p]
				if bestCard == bestHand[1]:
					winning.append(p)

		for p in winning:
			p.chipCount += self.pot / len(winning)

		for p in winning:
			p.handWinCounter += 1
		return [p.name for p in winning]

	def summarizeGame(self):
		print('')
		winners = self.checkWinner()

		for player in self.players:
			player.printPlayerInfo()
		print('Winning player(s):', ', '.join(winners))
	
	