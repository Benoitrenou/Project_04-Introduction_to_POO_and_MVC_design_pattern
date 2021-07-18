from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('db.json', indent=4)
players_table = db.table('players')
# players_table.truncate()
joueur = Query()

class PlayerManager:
    """Manager for DB"""

    def save(self, player, table=players_table):
        """Player saving method."""
        player.id = table.insert(player.serialize())
        players_table.update({"id" : player.id}, joueur.firstname == player.firstname)

    def update(self, field, value, player_id, query = joueur.id, table=players_table):
        table.update({field: int(value)}, query == player_id)
        
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
        return ['Firstname', 'Lastname', 'Birthday DD/MM/YYYY', 'Sex M/F', 'Ranking - Positive Integers']

    @classmethod
    def is_clean(cls, key, value):
        """Validate format of value depends on the key associated."""
        if key == 'Birthday DD/MM/YYYY':
            try:
                value == datetime.strptime(value, '%d/%m/%Y').strftime('%d/%m/%Y')
            except ValueError:
                return False
        elif key == 'Sex M/F':
            if value.capitalize() not in cls.SEX_POSSIBLE:
                return False
        elif key == 'Ranking - Positive Integers':
            try:
                int(value)
                if int(value) < 0:
                    return False
            except:
                return False
        else:
            return True
