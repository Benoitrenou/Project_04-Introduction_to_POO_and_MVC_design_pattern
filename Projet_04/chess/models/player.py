from datetime import datetime

SEX_POSSIBLE = ["M", "F"]

def validate_birthday(date_text):
	"""Vérifie validité du format de Player.birthday
	"""
	try:
		if date_text != datetime.strptime(date_text, '%d/%m/%Y').strftime('%d/%m/%Y'):
			raise ValueError
		return date_text
	except ValueError:
		return (f'ValueError : birthday should be in format DD/MM/YYYY')


def validate_sex(sex_text):
    """Vérifie validité de l'attribut Player.sex"""
    try:
        if sex_text not in SEX_POSSIBLE:
            raise ValueError
        return sex_text
    except ValueError:
        return f"ValueError : {sex_text} is not a valid sex"


class Player:
    def __init__(
        self, firstname, lastname, birthday, sex, ranking, tournament_point=0, id=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = validate_birthday(birthday)
        self.sex = validate_sex(sex)
        self.ranking = ranking
        self.tournament_point = tournament_point
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
