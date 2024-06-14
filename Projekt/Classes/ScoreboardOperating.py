import json
import os


class Scoreboard:
    def __init__(self, fileDir=os.getcwd() + "\\Scoreboard.json"):
        self.fileDir = fileDir
        self.scores = self.load_scores()

    def add_score(self, player_name, score):
        self.scores[player_name] = self.scores.get(player_name, 0) + score

    def subtract_score(self, player_name, score):
        self.scores[player_name] = self.scores.get(player_name, 0) - score

    def save_scores(self):
        with open(self.fileDir, "w") as file:
            json.dump(self.scores, file)

    def load_scores(self):
        try:
            with open(self.fileDir, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            file = open(self.fileDir, "x")
            return {}
        except json.decoder.JSONDecodeError:
            return {}
