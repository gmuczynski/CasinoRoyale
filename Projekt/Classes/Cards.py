# Classes/Cards.py
from .constans import values

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = values[value]

    def __str__(self):
        return f"{self.suit} {self.value} {self.suit}"
