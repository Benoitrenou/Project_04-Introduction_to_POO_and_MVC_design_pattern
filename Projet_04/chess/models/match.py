from .player import Player
from tinydb import TinyDB, Query

db = TinyDB("db.json", indent=4)
players_table = db.table("players")
joueur = Query()


class Match:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None

    def __repr__(self):
        return f"([{self.player_1.firstname}, {self.player_1.tournament_point}]," \
        f"[{self.player_2.firstname}, {self.player_2.tournament_point}])"

    def winner_is(self, result):
        """Modify both player.tournament_point depends on the result."""
        if result == 1:
            self.player_1.tournament_point += 1
            self.winner = self.player_1.id
        if result == 2:
            self.player_2.tournament_point += 1
            self.winner = self.player_2.id
        if result == 0:
            self.player_1.tournament_point += 0.5
            self.player_2.tournament_point += 0.5
            self.winner = 'Draw'
        return self.winner

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
        return {"player_1": self.player_1.id, "player_2": self.player_2.id, "winner":self.winner}

    @classmethod
    def deserialize(cls, data, table=players_table):
        """Return an instance of Match from JSON format written data."""
        player_1 = Player.deserialize(table.get(doc_id=data["player_1"]))
        player_2 = Player.deserialize(table.get(doc_id=data["player_2"]))
        match = cls(player_1, player_2)
        match.winner = data["winner"]
        return match
