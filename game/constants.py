BATCH_SIZE = 500
TOTAL_BUFFER_SIZE = 10 * BATCH_SIZE
STARTING_EPSILON = 0.99
EPSILON_MULTIPLIER = 0.99
NUM_ROUNDS = 2
ANTE = 1
BET = 2 * ANTE # 2
BET_NORM = BET * 8 # 16
REWARD_NORM = (2 * ANTE) + BET_NORM * NUM_ROUNDS # 2 + 16*2 = 34

dealSystem = [2]

commonCardSize = 3

suits = {0: "Hearts", 1: "Diamonds", 2: "Clubs", 3: "Spades"}

ranks = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}
