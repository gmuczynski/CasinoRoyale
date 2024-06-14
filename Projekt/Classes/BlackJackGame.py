# Classes/BlackJackGame.py
from .Decks import Deck
from .Hands import Hand
from .ScoreboardOperating import Scoreboard


class BlackJack:
    def gameLogic(self):
        print("Welcome to Blackjack!")

        win = False

        name = input("Enter your name or create new profile: ")

        scoreboard = Scoreboard()

        scoreboard.add_player(name)
        scoreboard.save_scores()

        deck = Deck(1)

        player_hand = Hand()
        player_hand_2 = None
        dealer_hand = Hand()

        print(f"You have {scoreboard.get_scores(name)} credits!")
        bet_amount = int(input("Enter your bet amount: "))
        scoreboard.subtract_score(name, bet_amount)
        scoreboard.save_scores()

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
                win = True
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
                win = True
                return
            elif player_hand_2 is not None and player_hand_2.value > 21:
                print("You busted on your second hand!")
                return

            if len(player_hand.cards) > 1 and player_hand.cards[0].rank == player_hand.cards[1].rank and player_hand_2 is None:
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
            elif (action == 't' and len(player_hand.cards) > 1 and
                  player_hand.cards[0].rank == player_hand.cards[1].rank and player_hand_2 is None):
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
                win = True
            elif dealer_hand.value > player_hand.value:
                if player_hand_2 is None:
                    print("Dealer wins!")
                else:
                    print("Dealer wins against your first hand!")
            elif dealer_hand.value < player_hand.value:
                if player_hand_2 is None:
                    print("You win!")
                    win = True
                else:
                    print("You win on your first hand!")
                    win = True
            else:
                if player_hand_2 is None:
                    print("It's a tie!")
                    scoreboard.add_score(name, bet_amount)
                    scoreboard.save_scores()
                else:
                    print("It's a tie on your first hand!")

        print("***************************************************")
        if player_hand_2 is not None and dealer_hand.value <= 21 and player_hand_2.value < 22:
            if dealer_hand.value < player_hand_2.value:
                print("You win on your second hand")
                win = True
                print("***************************************************")
            elif 21 >= dealer_hand.value > player_hand_2.value:
                print("Dealer win against your second hand")
                print("***************************************************")
        if win is True:
            scoreboard.add_score(name, bet_amount*2)
            scoreboard.save_scores()

    # print("Do you want to play again? Yes/No")
    #
    # answer = input()
    #
    # while answer != "Yes" and answer != "No":
    # answer = input()
    # if answer == "y":
    # gameLogic()
    # elif answer == "n":
    # print("Thank you for playing!")
    # exit()
    # else:
    # print("Please enter y or n")
