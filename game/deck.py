from card import Card
from constants import suits, ranks
import random

class Deck():
	def __init__(self):
		self.cards = self.createDeck()
		self.usedCards = []

	def createDeck(self):
		cards = []

		for suit in suits:
			for rank in ranks:
				cards.append(Card(suit, rank))

		return cards
	
	def selectRandomCard(self):
		card = random.choice(self.cards)
		self.usedCards.append(card)
		self.cards.remove(card)
		return card
	
	def removeCardsFromDeck(self, cardsToRemove):
		newCards = []
		for card in self.cards:
			removeMe = False
			for cardToRemove in cardsToRemove:
				if card.sameCard(cardToRemove):
					removeMe = True
					break

			if not removeMe:
				newCards.append(card)

		self.cards = newCards