from .match import Match

class Round:

	def __init__(self, name):
		self.matches = []
		self.name = name
		# self.date_time_start = date_time_start
		# self.date_time_end = date_time_end

	def __str__(self):
		return f'{self.name}'

	def __repr__(self):
		return f'{self.name}'

	def add_match(self, match):
		""" Ajoute un match à round.matches []
		"""
		self.matches.append(match)
		return self.matches

	def get_results(self):
		""" Exécute méthode winner_is () de la classe Match sur chaque match de round.matches[]
		"""
		for match in self.matches:
			match.winner_is()

	def serialize(self):
		""" Renvoie une écriture de Round adaptée au format JSON - Appelle méthode Match.serialize()
		"""
		matches = [match.serialize() for match in self.matches]
		return {
		'matches': matches,
		'name': self.name,
		}
		
	@classmethod
	def deserialize(cls, data):
		"""Crée une instance de Round à partir de données au format JSON
		"""
		round = cls(name=data['name'])
		for match in data['matches']:
			game = Match.deserialize(match)
			round.matches.append(game)
		return round