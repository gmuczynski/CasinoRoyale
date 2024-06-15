import json
import os


class Scoreboard:
    """
    Klasa reprezentująca obiekt w ktorym przechowywane są dane odnośnie graczy oraz
    ilości posiadanych przez nich kredytów
    """
    def __init__(self, fileDir=os.getcwd() + "\\Scoreboard.json"):
        self.fileDir = fileDir
        self.scores = self.load_scoreboard()

    def check_player(self, player_name):
        """
        Metoda sprawdza czy dany gracz istnieje już w pliku przechowującym dane

        Parametry:
        player_name

        Zwraca:
        W zależności od tego czy gracz znajduje się w pliku czy nie, true lub false
        """
        with open(self.fileDir, 'r') as file:
            data = json.load(file)
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(key, list):
                    for item in key:
                        if player_name in json.dumps(item):
                            return item
                elif player_name in json.dumps(key):
                    return True
        else:
            return False

    def add_score(self, player_name, score):
        """
        Metoda dodaje wynik okreslony w parametrze score do gracza określonego w parametrze player_name

        Parametry:
        player_name
        param score
        """
        self.scores[player_name] = self.scores.get(player_name, 0) + score

    def add_player(self, player_name):
        """
        Metoda dodaje gracza i dodaje na jego konto 1000 kredytów jeżeli gra po raz pierwszy lub wita go ponownie
        w zależności od wyniku metody check_player()

        Parametry:
        player_name
        """
        if self.check_player(player_name):
            print(f"Welcome back {player_name}!")
        else:
            print(f"Welcome {player_name}, here are your 1000 starting credits!")
            self.scores[player_name] = self.scores.get(player_name, 0) + 1000.0

    def subtract_score(self, player_name, score):
        """
        Metoda odejmuje wynik gracza w momencie w którym obstawia swoje kredyty

        Parametry:
        player_name
        score
        """
        if self.scores.get(player_name, 0) - score < 0 or score < 0:
            raise ValueError(f"You dont have enough credits or you tried to bet negative number!")
        else:
            self.scores[player_name] = self.scores.get(player_name, 0) - score

    def save_scores(self):
        """
        Metoda która zapisuje zmiany do pliku
        """
        with open(self.fileDir, "w") as file:
            json.dump(self.scores, file)

    def get_scores(self, player_name):
        """
        Metoda która ściąga aktualną liczbę kredytów gracza

        Paramtery
        player_name

        Zwraca:
        total_credit
        """
        total_credit = self.scores.get(player_name, 0)
        return total_credit

    def load_scoreboard(self):
        """
        Metoda która zczytuje dane z pliku json

        Zwraca:
        Słownik z danymi, jeżeli wystąpi jakikolwiek błąd, zwraca pusty słownik
        """
        try:
            with open(self.fileDir, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            file = open(self.fileDir, "x")
            return {}
        except json.decoder.JSONDecodeError:
            return {}
