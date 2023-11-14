from gameState import GameState
from player import Player
from collections import defaultdict
from gameExperience import gameExperience
from model import Model
from utils import expToFile
from constants import BATCH_SIZE, TOTAL_BUFFER_SIZE, STARTING_EPSILON

class PokerGame:
    def __init__(self, load_model, players, start_ante, bet_amount):
        self.model = Model(load_model=load_model)
        self.start_ante = start_ante
        self.gameState = GameState(players, start_ante)
        self.bet_amount = bet_amount
        self.game_experiences = defaultdict(list)
        self.experiences_counter = 0
        self.epsilon = STARTING_EPSILON

        self.actionFrequencies = [0,0,0]

        for i in range(15):
            print(i)
            self.playSimplePoker()
            gameExperiences = [gE.getRLInfo() for sublist in self.game_experiences.values() for gE in sublist]
            expToFile(gameExperiences)

            self.model.trainModel()
            self.epsilon *= 0.9
            self.experiences_counter = 0

            print(self.actionFrequencies)
            self.actionFrequencies = [0,0,0]
            
    def playSimplePoker(self):
        while self.experiences_counter < 5:
            self.gameState.startNewHand()
            self.roundOfBetting([])

            if (len(self.gameState.getActivePlayers()) > 1):  # if more than one player remains
                self.roundOfBetting(self.gameState.sharedCards)

            self.gameState.checkWinner()
            self.assignRewards()
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
                if (
                    not player.folded
                    and player.currentBet < self.gameState.currentRoundBet
                ):
                    # print("PLAYER", i, "HAS TO CALL OR FOLD")
                    self.playerTurn(player, sharedCards)

    def playerTurn(
        self, player, commonCards, options=["bet", "check", "fold", "raise"]
    ):
        playerOptions = options[:]
        playerIndex = player.index

        # don't fold or raise if not current bet (checking dominates folding)
        if self.gameState.currentRoundBet:
            playerOptions.remove("check")
        else: # can't check if there is already a bet
            playerOptions.remove("fold")

        # CREATE A GAME EXPERIENCE BASED ON THIS SITUATION
        newGameExperience = gameExperience(
            self.gameState.round,
            self.gameState.currentRoundBet,
            self.gameState.pot,
            player.hand.cards,
            commonCards,
        )

        action = self.model.chooseBestAction(self.epsilon, newGameExperience)
        self.actionFrequencies[action] += 1
        newGameExperience.setActionTaken(action)

        if self.gameState.round > 1:  # if not in the first round
            mostRecentExperience = self.game_experiences[playerIndex][-1]
            mostRecentExperience.setNextGameExperience(newGameExperience)

        self.game_experiences[playerIndex].append(newGameExperience)
        self.experiences_counter += 1

        ## CARRY OUT CHOSEN ACTION ##
        if action == 2:
            self.gameState.bet(playerIndex, self.bet_amount * 2)

        if action == 1:
            self.gameState.bet(playerIndex, self.bet_amount)

        if not action:
            if self.gameState.currentRoundBet: # fold
                self.gameState.fold(playerIndex)
            else: # check
                return

    def assignRewards(self):
        rewards = []

        # create a list of player rewards (chip win/loss this hand)
        for i, startingAmount in enumerate(self.gameState.startingChipAmounts):
            rewards.append(self.gameState.players[i].chipCount - startingAmount)

        # assign these rewards to their most recent game experiences
        # otherwise, the reward will remain at its default value of 0
        for i in range(len(self.gameState.players)):
            mostRecentExperience = self.game_experiences[i][-1]
            mostRecentExperience.setGameReward(rewards[i])

def main():
    player1 = Player("Rahul", 0, 0)
    player2 = Player("Zane", 1, 0)
    ante = 1
    betAmount = 2
    pg = PokerGame(
        load_model=False,
        players=[player1, player2],
        start_ante=ante,
        bet_amount=betAmount
    )

if __name__ == "__main__":
    main()
