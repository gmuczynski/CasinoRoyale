# Author 1: Grzegorz Muczyński (s27971)
# Author 2: Hubert Mosakowski (s28829)


import random

suits = ['♣', '♦', '♥', '♠']
# suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
          'Ace': 11}


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = values[value]

    def __str__(self):
        return f"{self.suit} {self.value} {self.suit}"


class Deck:
    def __init__(self, number_of_decks):
        # self.cards = [(Card(suit, value) for suit in suits for value in values) for _ in range(number_of_decks)]
        self.cards = [Card(suit, value) for suit in suits for value in values for _ in range(number_of_decks)]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


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
            self.aces -= -1

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


def blackjack():
    print("Welcome to Blackjack!")

    # player_name = input("What is your name? ")

    # print("Hello, " + player_name + "!")

    deck = Deck(2)

    player_hand = Hand()
    player_hand_2 = None
    dealer_hand = Hand()

    for _ in range(2):
        player_hand.add_card(deck.draw_card())
        dealer_hand.add_card(deck.draw_card())

    if dealer_hand == 21:
        print("Dealer has blackjack")
        return

    active_hand = 0

    while True:
        print("\nYour hand:", ' | '.join(str(card) for card in player_hand.cards),
              f"Value of hand: {player_hand.value}")

        if player_hand_2 is not None:
            print("\nYour second hand:", ' | '.join(str(card) for card in player_hand_2.cards),
                  f"Value of hand: {player_hand_2.value}")

        print("---------------------------------------------------\nDealer's hand: ", str(dealer_hand.cards[0]),
              "[Hidden]")

        if player_hand.value == 21:
            print("BLACKJACK! You win!")
            if player_hand_2 is None:
                return
            else:
                active_hand = 1
        elif player_hand.value > 21:
            print("You busted! Dealer wins.")
            if player_hand_2 is None:
                return
            else:
                active_hand = 1

        if player_hand_2 is not None and player_hand_2.value == 21:
            print("BLACKJACK! You win on your second hand!")
            return
        elif player_hand_2 is not None and player_hand_2.value > 21:
            print("You busted on your second hand! Dealer wins.")
            return

        if len(player_hand.cards) > 1 and player_hand.cards[0].rank == player_hand.cards[1].rank:
            action = input(f"Do you want to [H]it, [S]tand or Spli[T]?").strip().lower()
        else:
            action = input(f"Do you want to [H]it or [S]tand?").strip().lower()

        if action == 'h':
            if active_hand == 0:
                player_hand.add_card(deck.draw_card())
            elif player_hand_2 is not None:
                player_hand_2.add_card(deck.draw_card())
        elif action == 't':
            player_hand_2 = player_hand.split_hand()
        elif action == 's':
            if player_hand_2 is not None and active_hand == 0:
                active_hand = 1
            else:
                break

    print("\nDealer's hand:", ' | '.join(str(card) for card in dealer_hand.cards),
          f"Value of dealer hand: {dealer_hand.value}")
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.draw_card())
        print("Dealer draws ", str(dealer_hand.cards[-1]))
        print(f"Value of dealer hand: {dealer_hand.value}")

    if dealer_hand.value > 21:
        print("Dealer busted! You win!")
    elif dealer_hand.value > player_hand.value:
        print("Dealer wins!")
    elif dealer_hand.value < player_hand.value:
        print("You win!")
    else:
        print("It's a tie!")

    if player_hand_2 is not None:
        if dealer_hand.value < player_hand_2.value:
            print("You win on your second hand")
        elif 21 >= dealer_hand.value > player_hand_2.value:
            print("Dealer win against your second hand")


if __name__ == "__main__":
    blackjack()
