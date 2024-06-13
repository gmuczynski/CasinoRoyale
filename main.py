# Author 1: Grzegorz Muczyński (s27971)
# Author 2: Hubert Mosakowski (s28829)
import json
import os
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


class Scoreboard:
    def __init__(self, fileDir=os.getcwd() + "\\Scoreboard.json"):
        self.fileDir = fileDir
        self.scores = self.load_scores()

    def add_score(self, player_name, score):
        self.scores[player_name] = self.scores.get(player_name, 0) + score

    def subtract_score(self, player_name, score):
        self.scores[player_name] = self.scores.get(player_name, 0) - score

    def save_scores(self):
        with open(self.fileDir, "w") as file:
            json.dump(self.scores, file)

    def load_scores(self):
        try:
            with open(self.fileDir, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            file = open(self.fileDir, "x")
            return {}
        except json.decoder.JSONDecodeError:
            return {}


def blackjack():
    print("Welcome to Blackjack!")

    # player_name = input("What is your name? ")

    # print("Hello, " + player_name + "!")

    scoreboard = Scoreboard()
    scoreboard.add_score("Gregology", 20)
    scoreboard.add_score("Hubert", 25)
    scoreboard.subtract_score("Gregology", 15)
    scoreboard.save_scores()

    deck = Deck(1)

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
        print("---------------------------------------------------\nYour hand:", ' | '.join(str(card) for card in player_hand.cards),
              f"Value of hand: {player_hand.value}")

        if player_hand_2 is not None:
            print("---------------------------------------------------\nYour second hand:", ' | '.join(str(card) for card in player_hand_2.cards),
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
            if player_hand_2 is None:
                print("You busted! Dealer wins.")
            else:
                print("You busted on your first hand!")
            if player_hand_2 is None:
                return
            else:
                active_hand = 1

        if player_hand_2 is not None and player_hand_2.value == 21:
            print("BLACKJACK! You win on your second hand!")
            return
        elif player_hand_2 is not None and player_hand_2.value > 21:
            print("You busted on your second hand!")
            return

        if len(player_hand.cards) > 1 and player_hand.cards[0].rank == player_hand.cards[1].rank:
            action = input(f"Do you want to [H]it, [S]tand or Spli[T]?\t").strip().lower()
        else:
            if player_hand_2 is None:
                action = input(f"Do you want to [H]it or [S]tand?\t").strip().lower()
            else:
                if active_hand == 0:
                    action = input(f"Do you want to [H]it or [S]tand on your first hand?\t").strip().lower()
                elif active_hand == 1:
                    action = input(f"Do you want to [H]it or [S]tand on your second hand?\t").strip().lower()

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
        if player_hand.value <= 21 or player_hand_2.value <= 21:
            print(f"Value of dealer hand: {dealer_hand.value}")

    print("***************************************************")
    if player_hand.value < 22:
        if dealer_hand.value > 21:
            print("Dealer busted! You win!")
        elif dealer_hand.value > player_hand.value:
            if player_hand_2 is None:
                print("Dealer wins!")
            else:
                print("Dealer wins against your first hand!")
        elif dealer_hand.value < player_hand.value:
            if player_hand_2 is None:
                print("You win!")
            else:
                print("You win on your first hand!")
        else:
            if player_hand_2 is None:
                print("It's a tie!")
            else:
                print("It's a tie on your first hand!")

    print("***************************************************")
    if player_hand_2 is not None and dealer_hand.value <= 21 and player_hand_2.value < 22:
        if dealer_hand.value < player_hand_2.value:
            print("You win on your second hand")
            print("***************************************************")
        elif 21 >= dealer_hand.value > player_hand_2.value:
            print("Dealer win against your second hand")
            print("***************************************************")



if __name__ == "__main__":
    blackjack()
