from gameState import GameState
from player import Player
from collections import defaultdict
from gameExperience import gameExperience
import os
import json


class PokerGame:
    def __init__(self, players, start_ante, bet_amount):
        self.start_ante = start_ante
        self.gameState = GameState(players, start_ante)
        self.bet_amount = bet_amount
        self.game_experiences = defaultdict(list)

    def playSimplePoker(self):
        for _ in range(50):
            self.gameState.startNewHand()
            self.roundOfBetting([])

            if (
                len(self.gameState.getActivePlayers()) > 1
            ):  # if more than one player remains
                self.roundOfBetting(self.gameState.sharedCards)

            self.gameState.checkWinner()
            self.assignRewards()
            for playerIndex, gameExperiences in self.game_experiences.items():
                print(playerIndex)
                for gE in gameExperiences:
                    gE.summarizeGameExperience()
            self.gameState.summarizeGame()
            return

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
        if not self.gameState.currentRoundBet:
            playerOptions.remove("fold")

        # can't check if there is already a bet
        if self.gameState.currentRoundBet:
            playerOptions.remove("check")

        action = player.chooseAction(commonCards, playerOptions)

        # CREATE A GAME EXPERIENCE BASED ON THIS SITUATIONS
        newGameExperience = gameExperience(
            self.gameState.round,
            self.gameState.currentRoundBet,
            self.gameState.pot,
            player.hand.cards,
            commonCards,
        )

        # PROBABLY NEED TO TURN THESE ACTIONS INTO INDICES IN A LIST??
        newGameExperience.setActionTaken(action)

        if self.gameState.round > 1:  # if not in the first round
            mostRecentExperience = self.game_experiences[playerIndex][-1]
            mostRecentExperience.setNextGameExperience(newGameExperience)

        self.game_experiences[playerIndex].append(newGameExperience)

        ## CARRY OUT CHOSEN ACTION ##
        if action == "raise":
            self.gameState.bet(playerIndex, self.bet_amount * 2)

        if action == "bet":
            self.gameState.bet(playerIndex, self.bet_amount)

        if action == "check":
            return

        if action == "fold":
            self.gameState.fold(playerIndex)

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

    def expToFile(self, fileName="experiences.json"):
        gameExperiences = [gE for sublist in self.game_experiences.values() for gE in sublist]
        jsonOutput = [gE.getRLInfo(json=True) for gE in gameExperiences]
        
        with open(fileName, 'r') as file:
            previousExperiences = json.load(file)
        previousExperiences.extend(jsonOutput)
        
        with open(fileName, 'w') as file:
            json.dump(previousExperiences, file)

        # maybe adapt this to pandas CSV? whatever experience replay in tensorflow requires
        # try:
        # 	output_file = open("experiences.txt", "x")
        # except(FileExistsError):
        # 	output_file = open("experiences.txt", "w")
        # for player, exp in self.game_experiences.items():
        # 	output_file.write("Player " + str(player) + " experiences" + "\n" + "-" * 50 + "\n")
        # 	output_file.write("State	|	Action	|	Next State	|	Reward	\n")
        # 	for gE in exp:
        # 		expTuple = gE.getRLInfo()
        # 		for data in expTuple:
        # 			output_file.write(str(data) + "\t")
        # 		output_file.write("\n")
        # 		self.gameState.summarizeGame()
        # 	output_file.write("=" * 50 + "\n")
        # output_file.close()


def main():
    player1 = Player("Rahul", 0, 100)
    player2 = Player("Zane", 1, 100)
    ante = 5
    betAmount = 10
    pg = PokerGame([player1, player2], ante, betAmount)
    pg.playSimplePoker()
    pg.expToFile()


if __name__ == "__main__":
    main()
