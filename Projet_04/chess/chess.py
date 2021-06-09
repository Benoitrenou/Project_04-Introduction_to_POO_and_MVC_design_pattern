class Player:

	def __init__(self, last_name, first_name, birthday, sex, ranking):
		self.last_name = last_name
		self.first_name = first_name
		self.birthday = birthday
		self.sex = sex
		self.ranking = ranking

class Match:
	"""Chaque match consiste en une paire de joueurs avec un champ de résultats pour chaque joueur
	Un match unique doit être stocké sous la forme d'un tuple contenant deux listes,
	chacune contenant deux éléments : une référence à une instance de joueur et un score
	Les matchs multiples doivent être stockés sous forme de liste sur l'instance du tour.
	"""
    pass

class Round:
	"""Chaque tour est une liste de matchs
	En plus de la liste des correspondances, chaque instance du tour doit contenir un champ de nom
	Elle doit également contenir un champ Date et heure de début et un champ Date et heure de fin,
	qui doivent tous deux être automatiquement remplis lorsque l'utilisateur crée un tour et le marque comme terminé.
	Les instances de round doivent être stockées dans une liste sur l'instance de tournoi à laquelle elles appartiennent
	"""
	pass

class Tournament:
	"""Les instances de round doivent être stockées dans une liste sur l'instance de tournoi à laquelle elles appartiennent
	"""

    DEFAULT_ROUNDS_NUMBER = 4
    TIME_CONTROL = ['Bullet', 'Blitz', 'Coup rapide']

	def __init__(self, name, place, date_start, date_end, rounds_number=DEFAULT_ROUNDS_NUMBER, rounds_list, players, time_control, description):
		self.name = name
		self.place = place
		self.date_start = date_start
		self.date_end = date_end
		self.rounds_list = []
		self.players = []
		self.time_control = time_control
		self.description = description
