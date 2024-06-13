import random

from Classes.Cards import Card
from Classes.BlackJackGame import suits, values


class Deck:
    def __init__(self, number_of_decks):
        # self.cards = [(Card(suit, value) for suit in suits for value in values) for _ in range(number_of_decks)]
        self.cards = [Card(suit, value) for suit in suits for value in values for _ in range(number_of_decks)]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
