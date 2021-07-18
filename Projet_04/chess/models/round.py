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
		"""Add a match to round.matches."""
		self.matches.append(match)
		return self.matches

	def serialize(self):
		"""Return an instance of Round in JSON format written data."""
		matches = [match.serialize() for match in self.matches]
		return {
		'matches': matches,
		'name': self.name,
		}
		
	@classmethod
	def deserialize(cls, data):
		"""Return instance of Round from JSON format written data."""
		round = cls(name=data['name'])
		for match in data['matches']:
			game = Match.deserialize(match)
			round.matches.append(game)
		return round
