# Classes/BlackJackGame.py
import random
from .constans import suits, values
from .Bets import Bet

class BlackJack:
    def gameLogic(self):
        print("Welcome to Blackjack!")

        from .Decks import Deck
        from .Hands import Hand
        from .ScoreboardOperating import Scoreboard

        scoreboard = Scoreboard()
        scoreboard.add_score("Gregology", 20)
        scoreboard.add_score("Hubert", 25)
        scoreboard.subtract_score("Gregology", 15)
        scoreboard.save_scores()

        print("Scoreboard initialized and scores updated.")  # Debugging print

        deck = Deck(1)
        print("Deck created.")  # Debugging print

        player_hand = Hand()
        player_hand_2 = None
        dealer_hand = Hand()

        # Initialize the Bet class with a starting amount of money
        bet = Bet(1000)  # Initialize with 1000 units of money
        print("Initial total money written to file.")

        # Ask the player for a bet amount
        bet_amount = int(input("Enter your bet amount: "))
        bet.place_bet(bet_amount)  # Place the bet
        print("Bet placed and file updated.")

        for _ in range(2):
            player_hand.add_card(deck.draw_card())
            dealer_hand.add_card(deck.draw_card())

        if dealer_hand.value == 21:
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
                bet.add_winnings(bet_amount * 2)  # Add winnings
                return
            elif player_hand.value > 21:
                if player_hand_2 is None:
                    print("You busted! Dealer wins.")
                    return
                else:
                    print("You busted on your first hand!")
                    active_hand = 1

            if player_hand_2 is not None and player_hand_2.value == 21:
                print("BLACKJACK! You win on your second hand!")
                bet.add_winnings(bet_amount * 2)  # Add winnings
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
                bet.add_winnings(bet_amount * 2)  # Add winnings
            elif dealer_hand.value > player_hand.value:
                if player_hand_2 is None:
                    print("Dealer wins!")
                else:
                    print("Dealer wins against your first hand!")
            elif dealer_hand.value < player_hand.value:
                if player_hand_2 is None:
                    print("You win!")
                    bet.add_winnings(bet_amount * 2)  # Add winnings
                else:
                    print("You win on your first hand!")
                    bet.add_winnings(bet_amount * 2)  # Add winnings
            else:
                if player_hand_2 is None:
                    print("It's a tie!")
                else:
                    print("It's a tie on your first hand!")

        print("***************************************************")
        if player_hand_2 is not None and dealer_hand.value <= 21 and player_hand_2.value < 22:
            if dealer_hand.value < player_hand_2.value:
                print("You win on your second hand")
                bet.add_winnings(bet_amount * 2)  # Add winnings
                print("***************************************************")
            elif 21 >= dealer_hand.value > player_hand_2.value:
                print("Dealer win against your second hand")
                print("***************************************************")
