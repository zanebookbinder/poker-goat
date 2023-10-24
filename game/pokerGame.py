from gameState import GameState
from player import Player
from collections import defaultdict
from gameExperience import gameExperience

class PokerGame():
	def __init__(self, players, start_ante, bet_amount):
		self.start_ante = start_ante
		self.gameState = GameState(players, start_ante)
		self.bet_amount = bet_amount
		self.game_experiences = defaultdict(list)

	def playSimplePoker(self):
		for _ in range(50):
			self.gameState.startNewHand()
			self.roundOfBetting([])

			if len(self.gameState.getActivePlayers()) > 1:
				self.roundOfBetting(self.gameState.sharedCards)

			self.gameState.checkWinner()

		self.gameState.summarizeGame()

	def roundOfBetting(self, sharedCards):
		self.gameState.startNewRound()

		# ask everyone if they want to bet
		for i in range(len(self.gameState.players)):
			player = self.gameState.players[i]
			if player.folded:
				continue

			self.playerTurn(player, sharedCards)

		# if someone bet later on, go back through and make the other players bet or fold
		if self.gameState.currentRoundBet:
			for i in range(len(self.gameState.players)):
				player = self.gameState.players[i]
				if not player.folded and player.currentBet < self.gameState.currentRoundBet:
					# print("PLAYER", i, "HAS TO CALL OR FOLD")
					self.playerTurn(player, sharedCards)

	def playerTurn(self, player, commonCards, options = ['bet', 'check', 'fold', 'raise']):
		playerOptions = options[:]
		playerIndex = player.index

		# don't fold or raise if not current bet (checking dominates folding)
		if not self.gameState.currentRoundBet:
			playerOptions.remove('fold')

		# can't check if there is already a bet
		if self.gameState.currentRoundBet:
			playerOptions.remove('check')

		action = player.chooseAction(commonCards, playerOptions)

		if action == 'raise':
			# print("RAISE with cards:", [card.rank for card in player.hand.cards + sharedCards])
			self.gameState.bet(playerIndex, self.bet_amount * 2)

		if action == 'bet':
			self.gameState.bet(playerIndex, self.bet_amount)

		# if action == 'check':
		# 	return

		if action == 'fold':
			self.gameState.fold(playerIndex)
		
		# round, bettingLevel, pot, holeCards, commonCards
		newGameExperience = gameExperience(
			self.gameState.round,
			self.gameState.currentRoundBet,
			self.gameState.pot,
			player.hand.cards,
			commonCards
		)

		# PROBABLY NEED TO TURN THESE ACTIONS INTO INDICES IN A LIST??
		newGameExperience.setActionTaken(action)
		
def main():
	player1 = Player('Rahul', 0,  100)
	player2 = Player('Zane', 1, 100)
	ante = 5
	betAmount = 10
	pg = PokerGame([player1, player2], ante, betAmount)
	pg.playSimplePoker()
	
if __name__ == '__main__':
	main()