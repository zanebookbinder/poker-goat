from handRankUtil import compareAllHands
from deck import Deck

"""
This function compares a hand to all possible hands that an opponent could have
and checks the hand's winning percentage. Warning: this is very slow because 
there are many thousands of hands to check against.
"""
def scoreHand(holeCards, commonCards):
	fullDeck = Deck()
	fullDeck.removeCardsFromDeck(commonCards)

	thisHand = holeCards + commonCards

	wins = 0
	losses = 0

	for i in range(len(fullDeck.cards)):
		for j in range(i+1, len(fullDeck.cards)):
			card1 = fullDeck.cards[i]
			card2 = fullDeck.cards[j]

			possibleHand = [card1, card2] + commonCards
			winningHands = list(compareAllHands([thisHand, possibleHand]).keys())
			if len(winningHands) == 1:
				if not winningHands[0]:
					wins += 1
				else:
					losses += 1

	return wins / (wins + losses)
