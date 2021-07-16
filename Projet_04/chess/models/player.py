from tinydb import TinyDB, Query
from datetime import datetime

SEX_POSSIBLE = ["M", "F"]

def validate_birthday(date):
    """Vérifie validité du format de Player.birthday"""
    try:
        if date != datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y'):
            raise ValueError
        return date
    except ValueError:
        return (f'ValueError : birthday should be in format DD/MM/YYYY')

def validate_sex(sex):
    """Vérifie validité de l'attribut Player.sex"""
    try:
        if sex not in SEX_POSSIBLE:
            raise ValueError
        return sex
    except ValueError:
        return f"ValueError : {sex} is not a valid sex"

db = TinyDB('db.json', indent=4)
players_table = db.table('players')
# players_table.truncate()
joueur = Query()

class PlayerManager:
    """Manager for DB"""

    def save(self, player, table=players_table):
        """Player saving method"""
        player.id = table.insert(player.serialize())
        players_table.update({"id" : player.id}, joueur.firstname == player.firstname)

    def update(self, field, value, player_id, query = joueur.id, table=players_table):
        table.update({field: int(value)}, query == player_id)
        
class Player(PlayerManager):
    
    def __init__(
        self, firstname, lastname, birthday, sex, ranking, tournament_point=0, id=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = validate_birthday(birthday)
        self.sex = validate_sex(sex)
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
        """Retourne un dictionnaire de Player - format JSON"""
        return self.__dict__

    @classmethod
    def deserialize(cls, data):
        """Crée une instance de Player à partir de données au format JSON"""
        player = cls(**data)
        return player

    @classmethod
    def list_attributes(cls):
        return ['Firstname', 'Lastname', 'Birthday DD/MM/YYYY', 'Sex M/F', 'Ranking']
