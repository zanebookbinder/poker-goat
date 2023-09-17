from gameState import GameState
from player import Player
from card import Card

class PokerGame():
	def __init__(self, players, start_ante):
		self.start_ante = start_ante
		self.gameState = GameState(players, start_ante)

	def playSimplePoker(self):
		for _ in range(1000):
			self.gameState.startNewHand()
			self.playerTurn(self.gameState.players[0], ['bet', 'check'])
			self.playerTurn(self.gameState.players[1], ['call', 'check', 'fold'])
			self.gameState.checkWinner()

		for p in self.gameState.players:
			print(p.name, p.handWinCounter)
		self.gameState.summarizeGame()

	def playerTurn(self, player, options=['bet', 'check', 'fold', 'call', 'raise']):
		playerIndex = player.index

		# can't call if no current bet (that would be a check)
		if not self.gameState.currentRoundBet and 'call' in options:
			options.remove('call')

		# don't fold if not current bet (checking dominates folding)
		if not self.gameState.currentRoundBet and 'fold' in options:
			options.remove('fold')

		# can't check if there is already a bet
		if self.gameState.currentRoundBet and 'check' in options:
			options.remove('check')

		action = player.takeTurn(options)

		if action == 'bet':
			self.gameState.bet(playerIndex, 10)

		if action == 'check':
			return
		
		if action == 'call':
			self.gameState.call(playerIndex)

		if action == 'fold':
			self.gameState.fold(playerIndex)
		

def main():
	player1 = Player('Rahul', 0,  100)
	player2 = Player('Zane', 1, 100)
	ante = 5
	pg = PokerGame([player1, player2], ante)
	pg.playSimplePoker()
	

if __name__ == '__main__':
	main()