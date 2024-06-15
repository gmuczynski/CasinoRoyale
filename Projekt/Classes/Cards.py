from .constants import values


class Card:
    """
    Klasa która reprezentuje karty
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = values[value]

    def __str__(self):
        """
        Metoda która odpowiada za stworzenie karty jako obiektu

        Zwraca:
        suit value suit
        """
        return f"{self.suit} {self.value} {self.suit}"
