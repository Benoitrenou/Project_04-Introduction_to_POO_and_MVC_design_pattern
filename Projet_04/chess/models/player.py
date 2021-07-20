from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB("db.json", indent=4)
players_table = db.table("players")
# players_table.truncate()
joueur = Query()


class PlayerManager:
    """Manager for DB"""

    def save(self, player, table=players_table):
        """Player saving method."""
        player.id = table.insert(player.serialize())
        players_table.update({"id": player.id}, joueur.firstname == player.firstname)

    def update(self, field, value, player_id, query=joueur.id, table=players_table):
        """Player's database updating method."""
        table.update({field: int(value)}, query == player_id)

    def update_ranking(
        self, player_id, new_ranking, query=joueur.id, table=players_table
    ):
        """Player's ranking update method."""
        table.update({"ranking": int(new_ranking)}, query == player_id)

    @classmethod
    def alphabetic_players_report(cls, table=players_table):
        """Return a list of all players sorted by alphabetic order."""
        results = []
        for row in table:
            results.append(row)
        results.sort(key=lambda i: (i["lastname"], i["firstname"]))
        return results

    @classmethod
    def ranking_players_report(cls, table=players_table):
        """Return a list of all players sorted by ranking."""
        results = []
        for row in table:
            results.append(row)
        results.sort(key=lambda i: (i["ranking"]), reverse=True)
        return results

    @classmethod
    def search_by_id(cls, player_id, table=players_table):
        """Return JSON data of a player from database through his id."""
        return table.get(joueur.id == int(player_id))


class Player(PlayerManager):

    SEX_POSSIBLE = ["M", "F"]

    def __init__(
        self, firstname, lastname, birthday, sex, ranking, tournament_point=0, id=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.sex = sex
        self.ranking = int(ranking)
        self.tournament_point = int(tournament_point)
        self.id = id

    def __gt__(self, other):
        return (self.tournament_point, self.ranking) > (
            other.tournament_point,
            other.ranking,
        )

    def __eq__(self, other):
        return (self.tournament_point, self.ranking) == (
            other.tournament_point,
            other.ranking,
        )

    def __hash__(self):
        return hash(self.firstname)

    def __str__(self):
        return f"{self.firstname.capitalize()}"

    def __repr__(self):
        return f"{self.firstname}"

    def serialize(self):
        """Return a JSON format written version of Player."""
        return self.__dict__

    @classmethod
    def deserialize(cls, data):
        """Return instance of Player from JSON format written data."""
        player = cls(**data)
        return player

    @classmethod
    def list_attributes(cls):
        """Return a list of attributes required to instance Player."""
        return [
            "Firstname",
            "Lastname",
            "Birthday DD/MM/YYYY",
            "Sex M/F",
            "Ranking - Positive Integers",
        ]

    @classmethod
    def clean_attributes_infos(cls, key, value):
        """Validate format attributes for Player instanciation."""
        if key == "Birthday DD/MM/YYYY":
            try:
                value == datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                return False
        elif key == "Sex M/F":
            if value.capitalize() not in cls.SEX_POSSIBLE:
                return False
        elif key == "Ranking - Positive Integers":
            try:
                int(value)
                if int(value) < 0:
                    return False
            except ValueError:
                return False
        else:
            return True
