import json
import os
import random

from Classes.Decks import Deck
from Classes.Hands import Hand
from Classes.ScoreboardOperating import Scoreboard
from Classes.constans import values, suits


class BlackJack:

    def gameLogic(self):
        print("Welcome to Blackjack!")

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
        print("---------------------------------------------------\nYour hand:",
              ' | '.join(str(card) for card in player_hand.cards),
              f"Value of hand: {player_hand.value}")

        if player_hand_2 is not None:
            print("---------------------------------------------------\nYour second hand:",
                  ' | '.join(str(card) for card in player_hand_2.cards),
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
