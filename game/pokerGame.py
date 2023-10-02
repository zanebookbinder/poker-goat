from gameState import GameState
from player import Player

class PokerGame():
	def __init__(self, players, start_ante, bet_amount):
		self.start_ante = start_ante
		self.gameState = GameState(players, start_ante)
		self.bet_amount = bet_amount

	def playSimplePoker(self):
		for _ in range(5):
			self.gameState.startNewHand()
			print('First round of betting')
			self.roundOfBetting([])

			if not self.gameState.winner:
				print('Second round of betting')
				self.roundOfBetting(self.gameState.sharedCards)
			self.gameState.checkWinner()
			self.gameState.summarizeGame()

		for p in self.gameState.players:
			print(p.name, p.handWinCounter)
		self.gameState.summarizeGame()

	def roundOfBetting(self, sharedCards):
		self.gameState.startNewRound()

		# ask everyone if they want to bet
		for i in range(len(self.gameState.players)):
			player = self.gameState.players[i]
			if player.folded:
				print('player', i, 'has folded')
				continue

			self.playerTurn(player, sharedCards)

		# if someone bet later on, go back through and make the other players bet or fold
		if self.gameState.currentRoundBet:
			print('There were bets this round')
			for i in range(len(self.gameState.players)):
				player = self.gameState.players[i]
				if not player.folded and player.currentBet < self.gameState.currentRoundBet:
					print("PLAYER", i, "HAS TO CALL OR FOLD")
					self.playerTurn(player, sharedCards)

	def playerTurn(self, player, sharedCards):
		options = ['bet', 'check', 'fold']
		playerIndex = player.index

		# don't fold if not current bet (checking dominates folding)
		if not self.gameState.currentRoundBet and 'fold' in options:
			options.remove('fold')

		# can't check if there is already a bet
		if self.gameState.currentRoundBet and 'check' in options:
			options.remove('check')

		action = player.chooseAction(sharedCards, options)

		if action == 'bet':
			self.gameState.bet(playerIndex, self.bet_amount)

		if action == 'check':
			return

		if action == 'fold':
			self.gameState.fold(playerIndex)
		

def main():
	player1 = Player('Rahul', 0,  100)
	player2 = Player('Zane', 1, 100)
	ante = 5
	betAmount = 10
	pg = PokerGame([player1, player2], ante, betAmount)
	pg.playSimplePoker()
	
if __name__ == '__main__':
	main()