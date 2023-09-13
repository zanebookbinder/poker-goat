from gameState import GameState
from player import Player
from constants import dealSystem
from card import Card

class PokerGame():
	def __init__(self, players, start_ante):
		self.start_ante = start_ante
		self.gameState = GameState(players, start_ante)
		self.deal()

	def deal(self):
		numCardsToDeal = dealSystem[self.gameState.round]
		for _ in range(numCardsToDeal):
			for i in range(len(self.gameState.players)):
				nextCard = self.gameState.deck.selectRandomCard()
				self.gameState.players[i].receiveCard(nextCard)

	def playSimplePoker(self):
		self.playerTurn(self.gameState.players[0], ['bet', 'check'])
		self.playerTurn(self.gameState.players[1], ['call', 'check', 'fold'])
		self.gameState.summarizeGame()

	def playerTurn(self, player, options=['bet', 'check', 'fold', 'call', 'raise']):
		playerIndex = player.index

		if not self.gameState.currentRoundBet and 'call' in options:
			options.remove('call')
		if not self.gameState.currentRoundBet and 'fold' in options:
			options.remove('fold')
		if self.gameState.currentRoundBet and 'check' in options:
			options.remove('check')

		action = player.takeTurn(self.gameState, options)

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
	ante = 5
	pg = PokerGame([player1, player2], ante)
	pg.playSimplePoker()
	

if __name__ == '__main__':
	main()