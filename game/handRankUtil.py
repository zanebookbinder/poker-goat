from hand import Hand
from card import Card
from collections import Counter

"""
Hand rankings
1. Straight flush
2. Four of a kind
3. Full house
4. Flush
5. Straight
6. Three of a kind
7. Two pair
8. Pair
9. High card/Junk
"""

handTypeToValue = {
	"straight flush": 9,
	"four of a kind": 8,
	"full house": 7,
	"flush": 6,
	"straight": 5,
	"three of a kind": 4,
	"two pair": 3,
	"pair": 2,
	"junk": 1
}

def test():
	card1 = Card(0, 7)
	card2 = Card(1, 7)
	card3 = Card(2, 7)
	card4 = Card(3, 7)
	card5 = Card(2, 5)
	cards = [card1, card2, card3, card4, card5]
	return isFourOfAKind(cards)

# Helper methods #

def getCardValues(cards):
	return [card.rank for card in cards]

def getCardSuits(cards):
	return [card.suit for card in cards]

# Functions by possible hand type #
#######################################################

def isStraightFlush(cards):
	return isStraight(cards) and isFlush(cards)

def isFourOfAKind(cards):
	c = Counter(getCardValues(cards)) # {rank: count}
	if max([value for value in c.values()]) == 4:
		fourOfAKindCard = [rank for rank in c if c[rank] == 4][0]
		otherCard = [rank for rank in c if c[rank] == 1][0]
		hand = [fourOfAKindCard] * 4 + [otherCard]
		return ('four of a kind', hand)
	else:
		return ["fail"]

def isFullHouse(cards):
	c = Counter(getCardValues(cards))
	triple = pair = False
	for value in c.values():
		if value == 3:
			triple = True
		elif value == 2:
			pair = True
	return triple and pair

def isFlush(cards):
	suits = getCardSuits(cards)
	return len(set(suits)) == 1

def isStraight(cards):
	cardNumbers = sorted(getCardValues(cards))
	return cardNumbers == list(range(cardNumbers[0], cardNumbers[0] + 5))

def isThreeOfAKind(cards):
	c = Counter(getCardValues(cards))
	return max([value for value in c.values()]) == 3 and not isFullHouse(cards)

def isTwoPair(cards):
	c = Counter(getCardValues(cards)) # [2: 2, 7: 1, K: 2]
	pairs = 0
	for value in c.values():
		if value == 2:
			pairs += 1
	return pairs == 2
	
def isPair(cards):
	c = Counter(getCardValues(cards))
	return max([value for value in c.values()]) == 2 and not isTwoPair(cards)

##########################################################################################



def judgeHand(cards):
	return


if __name__ == "__main__":
	print(test())



##########################################################################################

def compareHands(handList):
    bestHand = handList[0]
    for hand in handList:
        #TODO
        pass