import json
import os


class Scoreboard:
    def __init__(self, fileDir=os.getcwd() + "\\Scoreboard.json"):
        self.fileDir = fileDir
        self.scores = self.load_scoreboard()

    def check_player(self, player_name):
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
        self.scores[player_name] = self.scores.get(player_name, 0) + score

    def add_player(self, player_name):
        if self.check_player(player_name):
            print(f"Welcome back {player_name}!")
        else:
            print(f"Welcome {player_name}, here are your 1000 starting credits!")
            self.scores[player_name] = self.scores.get(player_name, 0) + 1000

    def subtract_score(self, player_name, score):
        if self.scores.get(player_name, 0) - score < 0:
            raise ValueError(f"You dont have enough credits!")
        else:
            self.scores[player_name] = self.scores.get(player_name, 0) - score

    def save_scores(self):
        with open(self.fileDir, "w") as file:
            json.dump(self.scores, file)

    def get_scores(self, player_name):
        total_credit = self.scores.get(player_name, 0)
        return total_credit

    def load_scoreboard(self):
        try:
            with open(self.fileDir, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            file = open(self.fileDir, "x")
            return {}
        except json.decoder.JSONDecodeError:
            return {}
