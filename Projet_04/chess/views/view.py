from models.player import Player

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

	def get_player_informations(self):
		while True:
			new_player_attributes = []
			for item in Player.list_attributes():
				new_player_attributes.append(input(f"{item} ?"))
			return new_player_attributes

class CreateTournamentView:

	def get_tournament_informations(self):
		while True:
			new_tournament_attributes = []
			for item in Tournament.list_attributes():
				new_tournament_attributes.append(input(f"{item} ?"))
			return new_tournament_attributes

class PlayTournamentView:

	def get_tournament(self):
		while True:
			return (input('ID of tournament to be played ?'))
