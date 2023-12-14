# poker-goat by Zane Bookbinder and Rahul Dasgupta

### Overview
This repository contains the code for Reinforcement Learning with a Python-based 
game of Texas Hold'em, simplified to eliminate the turn and the river (only 
three common cards). It was created for our independent study during the Fall
of 2023 with Professor Dave Byrd at Bowdoin College.

### Repository Contents

**pokerGame.py:** the main Poker file. Contains the game structure and runs
play/train loops during which batches of games are played and then used to 
train the model

**gameState.py:** the state of a Poker game. Contains information about players,
cards, bets, etc. 

**gameExperience.py:** an (s,a,s',r) learning experience

**model.py:** a Keras RL model that uses GameExperiences to learn optimal actions

**player.py:** a Poker player that uses the Model to choose actions

**smartPlayer.py:** a Poker player that chooses actions probabilistically based
on simple hand strength

**deck.py:** a collection of 52 cards

**card.py:** a Card object with suit and rank properties

**cardAutoencoder.py:** a Keras autoencoder that reduces a 52-length array of 
1s and 0s (representing a deck) to 8 numerical outputs

**constants.py:** model training and general game constants

**hand.py:** a list of cards in a player's hand

**handRankUtil.py:** functions that evaluate the in-game strength of a Poker hand

**handScoreUtil.py:** a function that compares a Player's hand with all other 
possible hands and determines the probability of winning

**model_tester.py:** input examples to test the model's performance while training

**utils.py:** utility functions for reading from and writing to files

**/output:** log files for iterations of the model run on Bowdoin's HPC cluster

**experiences.json:** a json list containing the most recent GameExperience information
(to pick from when training the model)

**run_autoencoder.sh:** a Bash script to train the autoencoder on the HPC cluster

**run_model.sh:** a Bash script to train the model on the HPC cluster

**ALL OTHER DIRECTORIES:** contains various iterations of trained models
