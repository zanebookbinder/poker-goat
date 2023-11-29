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
	
	def selectBadCards(self, n):
		if n == 2:
			card1 = [c for c in self.cards if c.suit == 0 and c.rank == 2][0]
			card2 = [c for c in self.cards if c.suit == 1 and c.rank == 4][0]
			self.usedCards.append(card1)
			self.usedCards.append(card2)
			self.cards.remove(card1)
			self.cards.remove(card2)
			return [card1, card2]
		elif n == 3:
			card1 = [c for c in self.cards if c.suit == 0 and c.rank == 5][0]
			card2 = [c for c in self.cards if c.suit == 1 and c.rank == 6][0]
			card3 = [c for c in self.cards if c.suit == 2 and c.rank == 9][0]
			self.usedCards.append(card1)
			self.usedCards.append(card2)
			self.usedCards.append(card3)
			self.cards.remove(card1)
			self.cards.remove(card2)
			self.cards.remove(card3)
			return [card1, card2, card3]
		
	def selectGreatCards(self, n):
		if n == 2:
			card1 = [c for c in self.cards if c.suit == 0 and c.rank == 14][0]
			card2 = [c for c in self.cards if c.suit == 1 and c.rank == 14][0]
			self.usedCards.append(card1)
			self.usedCards.append(card2)
			self.cards.remove(card1)
			self.cards.remove(card2)
			return [card1, card2]
		elif n == 3:
			card1 = [c for c in self.cards if c.suit == 2 and c.rank == 14][0]
			card2 = [c for c in self.cards if c.suit == 3 and c.rank == 14][0]
			card3 = [c for c in self.cards if c.suit == 2 and c.rank == 13][0]
			self.usedCards.append(card1)
			self.usedCards.append(card2)
			self.usedCards.append(card3)
			self.cards.remove(card1)
			self.cards.remove(card2)
			self.cards.remove(card3)
			return [card1, card2, card3]
	
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