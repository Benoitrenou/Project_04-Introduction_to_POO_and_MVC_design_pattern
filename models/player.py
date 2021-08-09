from tinydb import TinyDB, Query


db = TinyDB("db.json", indent=4)
players_table = db.table("players")
query = Query()


class PlayerManager:
    """Object managing relationship Player-database."""

    def save(self, player, table=players_table):
        """Player saving method."""
        player.id = table.insert(player.serialize())
        players_table.update({"id": player.id}, query.firstname == player.firstname)

    def update(self, field, value, player_id, query=query.id, table=players_table):
        """Player's database updating method."""
        table.update({field: int(value)}, query == player_id)

    def update_ranking(
        self, player_id, new_ranking, query=query.id, table=players_table
    ):
        """Player's ranking update method."""
        table.update({"ranking": int(new_ranking)}, query == player_id)

    def all_players_report(self, table=players_table):
        """Return a list of all players data."""
        results = []
        for row in table:
            results.append(row)
        return results

    def search_by_id(self, player_id, table=players_table):
        """Return JSON data of a player from database through his id."""
        return table.get(query.id == int(player_id))


class Player:
    """Object Player."""

    SEX_POSSIBLE = ["M", "F"]

    def __init__(self, firstname, lastname, birthday, sex, ranking, tournament_point=0, id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.sex = sex
        self.ranking = int(ranking)
        self.tournament_point = int(tournament_point)
        self.id = id

    def __gt__(self, other):
        """Defines superiority between two instances of Player in sorting situation."""
        return (self.tournament_point, self.ranking) > (other.tournament_point, other.ranking)

    def __eq__(self, other):
        """Defines equality between two instances of Player in sorting situation."""
        return (self.tournament_point, self.ranking) == (other.tournament_point, other.ranking)

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
        return cls(**data)

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
