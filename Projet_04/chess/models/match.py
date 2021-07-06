from .player import Player

class Match:

	def __init__ (self, player_1, player_2):
		self.player_1 = player_1
		self.player_2 = player_2

	def __repr__(self):
		return f'([{self.player_1.firstname}, {self.player_1.tournament_point}], [{self.player_2.firstname}, {self.player_2.tournament_point}])'

	def winner_is (self):
		""" Demande gagnant du match via input à l'utilisateur
		Modifie les tournament_point en fonction du résultat de chaque joueur
		Si nul appelle méthode is_draw()
		"""
		winner = input(f'Quel est le gagnant 1- {self.player_1.firstname} ou 2 - {self.player_2.firstname} ?')
		if winner=='1':
			self.player_1.tournament_point += 1
		if winner=='2':
			self.player_2.tournament_point += 1
		if winner=='0':
			self.is_draw()

	def is_draw (self):
		""" Modifie tournament_point des joueurs += 0.5 pour match nul
		"""
		self.player_1.tournament_point += 0.5
		self.player_2.tournament_point += 0.5

	def __str__(self):
		return f'({self.player_1.firstname} vs {self.player_2.firstname})'

	def __eq__(self, other):
		return (
			(self.player_1.id, self.player_2.id) == (other.player_1.id, other.player_2.id)
			or (self.player_1.id, self.player_2.id) == (other.player_2.id, other.player_1.id))

	def serialize (self):
		""" Renvoie une écriture de Match adaptée au format JSON - Appelle méthode Player.serialize()
		"""
		player_1 = self.player_1.serialize()
		player_2 = self.player_2.serialize()
		return {
			'player_1': player_1,
			'player_2': player_2
		}

	@classmethod
	def deserialize (cls, data):
		""" Crée une instance de Match à partir de données au format JSON
		"""
		player_1 = Player.deserialize(data['player_1'])
		player_2 = Player.deserialize(data['player_2'])
		match = cls(player_1, player_2)
		return match