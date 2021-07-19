from .player import Player
from tinydb import TinyDB, Query

db = TinyDB("db.json", indent=4)
players_table = db.table("players")
joueur = Query()


class Match:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

    def __repr__(self):
        return f"([{self.player_1.firstname}, {self.player_1.tournament_point}], [{self.player_2.firstname}, {self.player_2.tournament_point}])"

    def winner_is(self, result):
        """Modify both player.tournament_point depends on the result."""
        if result == 1:
            self.player_1.tournament_point += 1
        if result == 2:
            self.player_2.tournament_point += 1
        if result == 0:
            self.player_1.tournament_point += 0.5
            self.player_2.tournament_point += 0.5

    def __str__(self):
        return f"({self.player_1.firstname.capitalize()} vs {self.player_2.firstname.capitalize()})"

    def __eq__(self, other):
        return (self.player_1.id, self.player_2.id) == (
            other.player_1.id,
            other.player_2.id,
        ) or (self.player_1.id, self.player_2.id) == (
            other.player_2.id,
            other.player_1.id,
        )

    def serialize(self):
        """Return a JSON format written version of Match."""
        return {"player_1": self.player_1.id, "player_2": self.player_2.id}

    @classmethod
    def deserialize(cls, data, table=players_table):
        """Return an instance of Match from JSON format written data."""
        match_data = []
        for reference, player_id in data.items():
            player = Player.deserialize(table.get(doc_id=player_id))
            match_data.append(player)
        match = cls(*match_data)
        return match
