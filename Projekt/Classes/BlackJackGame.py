from .Decks import Deck
from .Hands import Hand
from .ScoreboardOperating import Scoreboard


class BlackJack:
    """
    Klasa która zawiera w sobie logikę gry, cały przebieg rozgrywki dzieje się tutaj
    """
    pass


def game_logic():
    """
    Metoda zawierająca całą logikę gry

    Parametry:
    brak

    Zwraca:
    brak
    """
    print("Welcome to Blackjack!")
    name = input("Enter your name or create new profile: ")

    scoreboard = Scoreboard()

    scoreboard.add_player(name)
    scoreboard.save_scores()

    player_hand = Hand()
    player_hand_2 = None
    dealer_hand = Hand()

    print(f"You have {scoreboard.get_scores(name)} credits!")

    print("How many decks do you want play with? (less or equal to 4)")
    print("The reward multipliers varies depending on the number of decks of cards you choose!")
    print("For 1 deck, reward multiplier is 1,5")
    print("For 2 decks, reward multiplier is 1,75")
    print("For 3 decks, reward multiplier is 2")
    print("For 4 decks, reward multiplier is 2,25")

    number_of_decks = int(input())

    while True:
        if 5 <= number_of_decks or number_of_decks <= 0:
            number_of_decks = int(input("You have to pick between 1 and 4! "))
        else:
            break

    deck = Deck(number_of_decks)
    reward_multiplier = 1.25

    while number_of_decks != 0:
        reward_multiplier += 0.25
        number_of_decks -= 1

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
            add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
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
            add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
            return
        elif player_hand_2 is not None and player_hand_2.value > 21:
            print("You busted on your second hand!")
            return

        if len(player_hand.cards) > 1 and player_hand.cards[0].rank == player_hand.cards[
            1].rank and player_hand_2 is None:
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
            add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
        elif dealer_hand.value > player_hand.value:
            if player_hand_2 is None:
                print("Dealer wins!")
            else:
                print("Dealer wins against your first hand!")
        elif dealer_hand.value < player_hand.value:
            if player_hand_2 is None:
                print("You win!")
                add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
            else:
                print("You win on your first hand!")
                add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
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
            add_won_credits(bet_amount, name, reward_multiplier, scoreboard)
            print("***************************************************")
        elif 21 >= dealer_hand.value > player_hand_2.value:
            print("Dealer win against your second hand")
            print("***************************************************")


def add_won_credits(bet_amount, name, reward_multiplier, scoreboard):
    reward = bet_amount + (bet_amount * reward_multiplier)
    scoreboard.add_score(name, reward)
    scoreboard.save_scores()


