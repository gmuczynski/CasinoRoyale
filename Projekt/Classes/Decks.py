# Classes/Decks.py
from random import shuffle
from .Cards import Card
from .constants import suits, values

class Deck:
    def __init__(self, number_of_decks):
        self.cards = [Card(suit, value) for suit in suits for value in values for _ in range(number_of_decks)]
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
