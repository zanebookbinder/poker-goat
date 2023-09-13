from deck import Deck

class GameState():
	def __init__(self, players):
		self.players = players
		self.startNewHand()

	def startNewHand(self):
		self.pot = 0
		self.turn = 0
		self.round = 0
		self.deck = Deck()
		self.currentRoundBet = 0
		self.winner = None

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
			return [self.winner.name]
		
		activePlayers = self.getActivePlayers()
		bestHand = -1
		winning = []
		for p in activePlayers:
			if p.hand.calculateHandValue() > bestHand:
				bestHand = p.hand.calculateHandValue()
				winning = [p]
			elif p.hand.calculateHandValue() == bestHand:
				winning.append(p)

		for p in winning:
			p.chipCount += self.pot / len(winning)

		return [p.name for p in winning]


	def summarizeGame(self):
		print('')
		winners = self.checkWinner()

		for player in self.players:
			player.printPlayerInfo()
		print('Winning player(s):', ', '.join(winners))
	
	