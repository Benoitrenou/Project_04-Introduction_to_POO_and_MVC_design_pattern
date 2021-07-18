from models.player import Player
from models.tournament import Tournament

class HomeMenuView:

	def __init__(self, menu):
		self.menu = menu

	def _display_menu(self):
		for key, entry in self.menu.items():
			print (f'{key} : {entry.option}')

	def get_user_choice(self):
		while True:
			self._display_menu()
			choice = input(">>")
			if choice in self.menu:
				return self.menu[choice]

class CreatePlayerView:

	def get_player_informations(self, key):
		while True:
			value = input(f'{key} ?')
			return value

	def confirm_fields(self, fields):
		for field in fields:
			print (field)
		confirm = input('Confirm new player y/n ?')
		if confirm == 'y':
			return True
		else :
			print ('Creation of new player cancelled')
			return False

	def player_saved(self, player):
		print (f"Profil de {player.firstname.capitalize()} sauvegardé - ID : {player.id}")

	def invalid_value(self):
		print (f"Value invalid - Please respect format")

class CreateTournamentView:

	def get_tournament_informations(self):
		while True:
			new_tournament_attributes = []
			for item in Tournament.list_attributes():
				new_tournament_attributes.append(input(f"{item} ?\n"))
			return new_tournament_attributes

	def add_player_to_tournament(self):
		while True:
			player_id = input('Player ID ?')
			return player_id

	def new_tournament_created(self, new_tournament):
		print (f'{new_tournament.name} is now saved in database - ID = {new_tournament.id}')

class PlayTournamentView:

	def get_tournament(self):
		while True:
			return (input('ID of tournament to be played ?'))

	def present_matches(self, round):
		for match in round.matches:
				print (match)

	def play_match(self, match):
		while int(winner) != 0 or 1 or 2:
			winner = input(f'Who is the winner : 1- {match.player_1.firstname} | 2 - {match.player_2.firstname} | 0 - Draw ?')
		return int(winner)

	def update_classment(self, players):
		print (f'\nClassement actuel :')
		for player in players:
			print (f'{player.firstname.capitalize()} avec {player.tournament_point} points - Ranking = {player.ranking}')
		print ('\n')


