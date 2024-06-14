# Classes/Bets.py
class Bet:
    def __init__(self, initial_amount, file_path='betting_info.txt'):
        self.total_money = initial_amount
        self.file_path = file_path
        self.write_initial_amount()

    def write_initial_amount(self):
        with open(self.file_path, 'w') as file:
            file.write(f"Total money: {self.total_money}\n")

    def place_bet(self, bet_amount):
        if bet_amount > self.total_money:
            raise ValueError("Bet amount exceeds total money available")
        self.total_money -= bet_amount
        self.update_file()

    def add_winnings(self, winnings_amount):
        self.total_money += winnings_amount
        self.update_file()

    def update_file(self):
        with open(self.file_path, 'w') as file:
            file.write(f"Total money: {self.total_money}\n")
