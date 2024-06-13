class Bets:
    def __init__(self, total_amount, bet_amount, file_path="bet.txt"):
        self.total_amount = total_amount
        self.bet_amount = bet_amount
        self.file_path = file_path
        self.save_money_amount()

    def get_total_amount(self): #DO WYSWIETLANIA OBECNEJ ILOSCI POZOSTALYCH PIENIEDZY
        return self.total_amount

    def save_money_amount(self):
        with open(self.file_path, 'w') as file:
            file.write(f"{self.total_amount}\n")

    def add_winnings(self, bet_amount):
        self.total_amount += (bet_amount*2)
        self.save_money_amount()

    def place_bet(self, bet_amount):
        if bet_amount > self.total_amount:
            raise ValueError("Bet amount must be less than total amount")
        self.total_amount -= bet_amount
        self.save_money_amount()
