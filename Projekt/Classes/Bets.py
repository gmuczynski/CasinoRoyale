import os

class Bet:
    def __init__(self, initial_amount, file_path='bet.txt'):
        self.total_money = initial_amount
        self.file_path = file_path

    def update_money_file(self):
        with open(self.file_path, 'r') as file:
            file_content = int(file.read().strip())

        if file_content is not None:
            self.total_money = file_content
        else:
            with open(self.file_path, 'w') as file:
                file.write(f"{self.total_money}\n")

    def place_bet(self, bet_amount):
        if bet_amount > self.total_money:
            raise ValueError("Bet amount exceeds total money available")
        self.total_money -= bet_amount
        self.update_money_file()

    def add_winnings(self, winnings_amount):
        self.total_money += winnings_amount
        self.update_money_file()

# if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
#     with open(self.file_path, 'r') as file:
#         total_money = int(file.read().strip())
# else:
#     with open(self.file_path, 'w') as file:
#         file.write(f"{self.total_money}\n")
