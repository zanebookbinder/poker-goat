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
	cards1 = [
		Card(1, 7),
		Card(1, 8),
		Card(1, 9),
		Card(1, 10),
		Card(1, 11)
	]

	cards2 = [
		Card(1, 7),
		Card(1, 7),
		Card(2, 7),
		Card(3, 8),
		Card(1, 8)
	]

	return compareAllHands([cards1, cards2])

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
	return max([value for value in c.values()]) == 4
	
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

def sortCards(cards):
	if isFlush(cards) and not isFullHouse(cards) and not isFourOfAKind(cards): # sort cards by Rank only
		values = getCardValues(cards)
		values.sort(reverse=True)
		return values
	c = Counter(getCardValues(cards))
	ranksAndCounts = [(rank, count) for rank, count in c.items()]

	# sort cards by count first, then Rank (both descending)
	ranksAndCounts.sort(key=lambda x: (-x[1], -x[0]))
	output = []
	for rank, count in ranksAndCounts:
		output.extend([rank] * count)
	return output

def judgeHand(cards):
	hand = sortCards(cards)
	if isStraightFlush(cards):
		return ("straight flush", hand)
	elif isFourOfAKind(cards):
		return ("four of a kind", hand)
	elif isFullHouse(cards):
		return ("full house", hand)
	elif isFlush(cards):
		return ("flush", hand)
	elif isStraight(cards):
		return ("straight", hand)
	elif isThreeOfAKind(cards):
		return ("three of a kind", hand)
	elif isTwoPair(cards):
		return ("two pair", hand)
	elif isPair(cards):
		return ("pair", hand)
	else:
		return ("junk", hand)
	
##########################################################################################

def compareIdenticalHands(hand1, hand2):
	for i in range(len(hand1)):
		if hand1[i] > hand2[i]:
			return 1 # hand 1 wins
		elif hand1[i] < hand2[i]:
			return -1 # hand 2 wins	
	return 0 # tie

# handList: 2D list of cards
def compareAllHands(cardsList):
	judgedCards = [judgeHand(cards) for cards in cardsList]
	bestHands = [judgedCards[0]]
	bestHandIndices = [0]

	for i, (type, hand) in enumerate(judgedCards[1:]):
		if handTypeToValue[type] > handTypeToValue[bestHands[0][0]]:
			bestHands = [(type, hand)]
			bestHandIndices = [i+1]
		elif handTypeToValue[type] == handTypeToValue[bestHands[0][0]]:
			winner = compareIdenticalHands(bestHands[0][1], hand)
			if winner == -1:
				bestHands = [(type, hand)]
				bestHandIndices = [i+1]
			if not winner:
				bestHands.append((type, hand))
				bestHandIndices.append(i+1)

	return {bestHandIndices[i]: bestHands[i] for i in range(len(bestHandIndices))}

if __name__ == "__main__":
	print(test())
