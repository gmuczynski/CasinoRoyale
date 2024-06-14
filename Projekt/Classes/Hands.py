# Classes/Hands.py
from .constants import values
from .Cards import Card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bet = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.value]
        if card.value == "Ace":
            self.aces += 1
            self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def calculate_value(self):
        val = 0
        for card in self.cards:
            val += values[card.value]

        self.value = val

        self.adjust_for_ace()

    def split_hand(self):
        new_hand = Hand()
        new_hand.add_card(self.cards[1])
        self.cards.remove(self.cards[1])
        self.calculate_value()
        return new_hand
