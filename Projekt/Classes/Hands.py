from .constants import values


class Hand:
    """
    Klasa reprezentująca rękę w której trzymamy karty
    """
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bet = 0

    def add_card(self, card):
        """
        Metdoa dodaje kartę do ręki gracza

        Parametry:
        card
        """
        self.cards.append(card)
        self.value += values[card.value]
        if card.value == "Ace":
            self.aces += 1
            self.adjust_for_ace()

    def adjust_for_ace(self):
        """
        Metoda zmienia wartość asa z 11 na 1 w przypadku kiedy jest to dla gracza lepsze wyjście
        """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def calculate_value(self):
        """
        Metoda oblicza wartość punktową karty
        """
        val = 0
        for card in self.cards:
            val += values[card.value]

        self.value = val

        self.adjust_for_ace()

    def split_hand(self):
        """
        Metoda rozdziela karty gracza na dwie ręce, jedną kartę zostawia w ręce nr 1, a druga usuwa z pierwszej ręki
        i dodaje do drugiej
        :return:
        new_hand
        """
        new_hand = Hand()
        new_hand.add_card(self.cards[1])
        self.cards.remove(self.cards[1])
        self.calculate_value()
        return new_hand

