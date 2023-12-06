from gameState import GameState
from player import Player
from collections import defaultdict
from gameExperience import gameExperience
from model import Model
from utils import expToFile
from constants import BATCH_SIZE
from smartPlayer import SmartPlayer
import sys
from card import Card
import random

class PokerGame:
    def __init__(self, num_batches, load_model, players, start_ante, bet_amount):
        self.model = Model(load_model=load_model)
        self.start_ante = start_ante
        self.gameState = GameState(players, start_ante)
        self.bet_amount = bet_amount
        self.game_experiences = defaultdict(list)
        self.experiences_counter = 0

        self.actionFrequencies = [0,0,0]
        self.mostRecentActionRewards = [0,0,0]
        self.wLByAction = [[0,0], [0,0,], [0,0]]
        self.raiseFoldWins = 0
        self.betFoldWins = 0

        for i in range(num_batches):
            print('\n')
            print(i)
            self.playSimplePoker()
            gameExperiences = [gE.getRLInfo() for sublist in self.game_experiences.values() for gE in sublist]
            expToFile(gameExperiences)

            self.model.trainModel()
            self.experiences_counter = 0
            
    def playSimplePoker(self):
        self.handsPlayed = 0
        while self.experiences_counter < BATCH_SIZE:
            self.handsPlayed += 1
            self.gameState.startNewHand()
            self.roundOfBetting([])

            if (len(self.gameState.getActivePlayers()) > 1):  # if more than one player remains
                self.roundOfBetting(self.gameState.sharedCards)

            winnerDict = self.gameState.checkWinner()
            self.assignRewards(winnerDict)

        print('Hands played:', self.handsPlayed)
        print('Most recent action rewards:', self.mostRecentActionRewards)
        print('Action frequencies:', self.actionFrequencies)
        print('Expected reward per action:', [self.mostRecentActionRewards[i] / max(self.actionFrequencies[i], 1) for i in range(3)])
        print('W,L by action:', self.wLByAction)
        print('Total rewards:', sum([sum(self.wLByAction[i]) for i in range(3)]))
        print('Raise-fold wins:', self.raiseFoldWins)
        print('Bet-fold wins: ', self.betFoldWins)
        
        self.handsPlayed = 0
        self.actionFrequencies = [0,0,0]
        self.mostRecentActionRewards = [0,0,0]
        self.wLByAction = [[0,0], [0,0,], [0,0]]
        self.raiseFoldWins = 0
        self.betFoldWins = 0

    def roundOfBetting(self, sharedCards):
        self.gameState.startNewRound()

        # ask everyone if they want to bet
        for player in self.gameState.getActivePlayers():
            self.playerTurn(player, sharedCards, False)

        

        # if self.gameState.players[0].currentBet > self.gameState.players[1].currentBet and self.gameState.players[1].folded == False:
        #     print("THIS SHOULD NOT BE HAPPENINGGGGGG")



        activePlayerBets = [p.currentBet for p in self.gameState.getActivePlayers()]
        
        # if someone bet later on, go back through and make the other players bet or fold
        while len(set(activePlayerBets)) > 1:
            for player in self.gameState.getActivePlayers():
                if player.currentBet < self.gameState.currentRoundBet:
                    self.playerTurn(player, sharedCards, False)

            activePlayerBets = [p.currentBet for p in self.gameState.getActivePlayers()]

    def playerTurn(
        self, player, commonCards, verbose=False
    ):
        playerIndex = player.index

        # CREATE A GAME EXPERIENCE BASED ON THIS SITUATION
        newGameExperience = gameExperience(
            self.gameState.round,
            self.gameState.currentRoundBet,
            self.gameState.pot,
            player.hand.cards,
            commonCards,
        )

        action = player.chooseBestAction(self.model, newGameExperience, commonCards)

        # FAKE GAME WITH 10, 0, -10 REWARDS
        # rewards = [10, 0, -10]
        # newGameExperience.setGameReward(rewards[action])
        
        # ONLY DO THIS FOR NON-SMART PLAYER
        if not player.index:

            self.actionFrequencies[action] += 1
            newGameExperience.setActionTaken(action)

            # If there is a prior experience from this hand
            if player.hasTakenATurnThisHand:
                mostRecentExperience = self.game_experiences[playerIndex][-1]
                mostRecentExperience.setNextGameExperience(newGameExperience)

            self.game_experiences[playerIndex].append(newGameExperience)
            self.experiences_counter += 1

            player.hasTakenATurnThisHand = True

        amountToStayIn = self.gameState.currentRoundBet - player.currentBet

        ## CARRY OUT CHOSEN ACTION ##
        if amountToStayIn > 0:
            if action == 2: # raise on other players' bet
                if verbose:
                    print('raising on other players bet')
                self.gameState.bet(playerIndex, amountToStayIn * 2)

            elif action == 1: # call other players' bet
                if verbose:
                    print('calling other players bet')
                self.gameState.bet(playerIndex, amountToStayIn)

            elif not action: # fold
                if verbose:
                    print('would have to spent money to stay in, folding now')
                self.gameState.fold(playerIndex)
        else:
            if action == 2: # bet a lot
                if verbose:
                    print('betting a lot (didnt have to)')
                self.gameState.bet(playerIndex, self.bet_amount * 2)

            elif action == 1: # bet a little
                if verbose:
                    print('betting a little bit(didnt have to)')
                self.gameState.bet(playerIndex, self.bet_amount)

            elif not action: # check
                if verbose:
                    print('checking')
                return

    def assignRewards(self, winnerDict):
        rewards = []

        # create a list of player rewards (chip win/loss this hand)
        for i, startingAmount in enumerate(self.gameState.startingChipAmounts):
            rewards.append(self.gameState.players[i].chipCount - startingAmount)

        # assign these rewards to their most recent game experiences
        # otherwise, the reward will remain at its default value of 0
        for i in range(len(self.gameState.players)):
            if not self.gameState.players[i].index:
                mostRecentExperience = self.game_experiences[i][-1]
                mostRecentExperience.setGameReward(rewards[i])
            
                actionTaken = mostRecentExperience.action
                self.mostRecentActionRewards[actionTaken] += rewards[i]

                if rewards[i] > 0:
                    self.wLByAction[actionTaken][0] += 1
                elif rewards[i] < 0:
                    self.wLByAction[actionTaken][1] += 1

                if actionTaken == 2 and 'wins as the only remaining player' in winnerDict.values():
                    self.raiseFoldWins += 1

                if actionTaken == 1 and 'wins as the only remaining player' in winnerDict.values():
                    self.betFoldWins += 1

def main(num_batches):
    player1 = Player("Rahul", 0, 0)
    player2 = SmartPlayer("Zane", 1, 0)
    ante = 1
    betAmount = 2

    PokerGame(
        num_batches=int(num_batches),
        load_model=False,
        players=[player1, player2],
        start_ante=ante,
        bet_amount=betAmount
    )

if __name__ == "__main__":
    main(sys.argv[1])
