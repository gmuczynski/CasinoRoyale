# Author 1: Grzegorz Muczyński (s27971)
# Author 2: Hubert Mosakowski (s28829)


from Classes.BlackJackGame import BlackJack, game_logic

if __name__ == "__main__":
    game = BlackJack()
    game_logic()

answer = ""

while answer != "Yes" or answer != "No":
    print("Do you want to play again? Yes/No")
    answer = input()

    if answer == "Yes":
        game_logic()
    elif answer == "No":
        print("Thank you for playing!")
        exit()
    else:
        print("Please enter y or n")
