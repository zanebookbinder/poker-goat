from gameState import GameState
from player import Player
from constants import dealSystem

class PokerGame():
	def __init__(self, players):
		self.gameState = GameState(players)
		self.deal()

	def deal(self):
		numCardsToDeal = dealSystem[self.gameState.round]
		for _ in range(numCardsToDeal):
			for i in range(len(self.gameState.players)):
				nextCard = self.gameState.deck.selectRandomCard()
				self.gameState.players[i].receiveCard(nextCard)

	def playSimplePoker(self):
		self.playerTurn(0, ['bet', 'check'])
		self.playerTurn(1, ['call', 'check', 'fold'])
		self.gameState.summarizeGame()

	def playerTurn(self, playerIndex, options=['bet', 'check', 'fold', 'call', 'raise']):
		if not self.gameState.currentRoundBet and 'call' in options:
			options.remove('call')
		if self.gameState.currentRoundBet and 'check' in options:
			options.remove('check')

		action = self.gameState.players[playerIndex].takeTurn(self.gameState, options)

		if action == 'bet':
			self.gameState.bet(playerIndex, 10)

		if action == 'check':
			return
		
		if action == 'call':
			self.gameState.call(playerIndex)

		if action == 'fold':
			self.gameState.fold(playerIndex)
		

	
def main():
	player1 = Player('Olivia', 0,  100)
	player2 = Player('Zane', 1, 100)
	pg = PokerGame([player1, player2])
	pg.playSimplePoker()
	

if __name__ == '__main__':
	main()