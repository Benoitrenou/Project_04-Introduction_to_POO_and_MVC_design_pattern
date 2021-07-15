from itertools import repeat
from .round import Round
from .player import Player
from .match import Match
from tinydb import TinyDB, Query

db = TinyDB('db.json', indent=4)
tournaments_table = db.table('tournaments')
# tournaments_table.truncate()
players_table = db.table('players')
query = Query()

class TournamentManager:

    def save(self, tournament, table=tournaments_table):
        """Tournament's saving method"""
        tournament.id = table.insert(tournament.serialize())
        tournaments_table.update({"id" : tournament.id}, query.name == tournament.name)

    def end_round_update(self, tournament, table=tournaments_table):
    	"""Tournament's database updating method"""
    	updated_rounds = [round.serialize() for round in tournament.rounds]
    	updated_matches = [match.serialize() for match in tournament.matches_already_played]
    	tournaments_table.update({"rounds" : updated_rounds}, query.name == tournament.name)
    	tournaments_table.update({"matches_already_played" : updated_matches}, query.name == tournament.name)
    	tournaments_table.update({"current_round" : tournament.current_round}, query.name == tournament.name)

class Tournament (TournamentManager):

	ROUND_NUMBER=1
	DEFAULT_NUMBER_OF_PLAYERS = 8
	DEFAULT_NUMBER_OF_ROUNDS = 4

	def __init__(self, name):
		self.name = name
		self.rounds = []
		self.players = []
		self.matches_already_played = []
		self.current_round = 0
		self.number_of_players = self.DEFAULT_NUMBER_OF_PLAYERS
		self.number_of_rounds = self.DEFAULT_NUMBER_OF_ROUNDS

	def add_player(self, ref_joueur, players_table):
		"""Ajoute un joueur depuis players_table avec son doc_id"""
		self.players.append(Player.deserialize(players_table.get(doc_id=float(ref_joueur))))
		for player in self.players:
			player.tournament_point = 0

	def play(self):
		"""Tournament's playing method"""
		while self.current_round != self.number_of_rounds:
			if self.current_round == 0:
				self._play_first_round()
			else :
				self._play_next_round()

	def _play_first_round(self):
		"""First round's playing method"""
		for player in self.players:
			player.tournament_point = 0
		self.current_round += 1
		self.get_classment()
		self.round = Round (f'Round {str(self.current_round)}')
		self.rounds.append(self.round)
		half_index = int(self.DEFAULT_NUMBER_OF_PLAYERS/2)
		players_first_half = self.players[:half_index]
		players_second_half = self.players[half_index:]
		for match in zip(players_first_half, players_second_half):
			match = Match (match[0], match[1])
			self.matches_already_played.append(match)
			self.round.add_match (match)
		print (f'Rencontres {self.round.name}:')
		for item in self.round.matches:
			print (item)
		self.round.get_results()
		self.get_classment()
		self.end_round_update(self)

	def _play_next_round(self):
		"""Other rounds than first one playing method"""
		self.current_round += 1
		self._sort_players()
		self.round = Round (f'Round n°{self.current_round}')
		self.rounds.append(self.round)
		round_players = self.players[:]
		while len(round_players) != 0:
			player, *others = round_players
			for match in zip(repeat(player), others):
				match = Match (match[0], match[1])
				if match not in self.matches_already_played:
					round_players.remove(match.player_1)
					round_players.remove(match.player_2)
					self.matches_already_played.append(match)
					self.round.add_match (match)
					break
		print (f'Rencontres {self.round.name}:')
		for item in self.round.matches:
			print (item)
		self.round.get_results()
		self.get_classment()
		self.end_round_update(self)

	def _sort_players(self):
		"""Sorting players method"""
		self.players = sorted(self.players, reverse=True)
		return self.players

	def get_classment(self, players_table, query):
		# à déplacer dans controler via méthode sort_players()
		"""Print classement des joueurs selon méthode sort_players()
		"""
		print (f'Classement actuel :')
		for player in self._sort_players():
			players_table.update({"tournament_point" : player.tournament_point}, query.firstname == player.firstname)
			print (f'{player.firstname.capitalize()} avec {player.tournament_point} points')
		print ('')

	def serialize(self):
		""" Renvoie une écriture de Tournament adaptée au format JSON 
		Appelle méthodes Round.serialize() et Match.serialize()
		"""
		players = [player.id for player in self.players]
		rounds = [round.serialize() for round in self.rounds]
		matches = [match.serialize() for match in self.matches_already_played]
		return {
			'name': self.name,
			'rounds': rounds, 
			'players': players,
			'matches_already_played': matches,
			'current_round':self.current_round
		}

	@classmethod
	def deserialize(cls, tournament_id, tournaments_table=tournaments_table, players_table=players_table):
		""" Crée une instance de Tournament à partir de données au format JSON
		"""
		data = tournaments_table.get(doc_id=int(tournament_id))
		tournament = cls(name=data['name'])
		for player_id in data['players']:
			joueur = Player.deserialize(players_table.get(doc_id=player_id))
			tournament.players.append(joueur)
		for round in data['rounds']:
			tour = Round.deserialize(round)
			tournament.rounds.append(tour)
		for match in data['matches_already_played']:
			game = Match.deserialize(match)
			tournament.matches_already_played.append(game)
		tournament.current_round=data['current_round']
		return tournament

	@classmethod
	def list_attributes(cls):
		return ['Name']