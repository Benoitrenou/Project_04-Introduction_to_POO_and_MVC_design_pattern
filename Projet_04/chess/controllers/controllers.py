from models.player import Player
from models.tournament import Tournament
from utils.menus import Menu
from views.view import *

class ApplicationController:

	def __init__(self):
		self.controller = None

	def start(self):
		self.controller = HomeMenuController()
		while self.controller:
			self.controller = self.controller()

class HomeMenuController:

	def __init__(self):
		self.menu = Menu()
		self.view = HomeMenuView(self.menu)

	def __call__(self):
		self.menu.add("auto", "Créer un joueur", CreatePlayerController)
		self.menu.add("auto", "Créer un tournoi", CreateTournamentController)
		self.menu.add("auto", 'Jouer un tournoi', PlayTournamentController)
		self.menu.add("q", "Quitter l'application", EndScreenController)
		user_choice = self.view.get_user_choice()
		return user_choice.handler

class CreatePlayerController:

	def __init__(self):
		self.view = CreatePlayerView()

	def __call__(self):
		new_player_attributes = self.view.get_player_informations()
		new_player = Player(*new_player_attributes)
		new_player.player_manager.save()
		print (f'{new_player} is now saved in database - ID = {new_player.id}')
		# print dans controller à passer dans view
		return HomeMenuController

class CreateTournamentController:
	
	def __init__(self):
		self.view = CreateTournamentView()

	def __call__(self):
		new_tournament_attributes = self.view.get_tournament_informations()
		new_tournament = Tournament(*new_tournament_attributes)
		while len(new_tournament.players) != new_tournament.number_of_players:
			new_tournament.add_player(input('Player ID ?'))
		new_tournament.save(new_tournament)
		print (f'{new_tournament.name} is now saved in database - ID = {new_tournament.id}')
		# print in a controller - pass in a view
		return HomeMenuController	

class PlayTournamentController:

	def __init__(self):
		self.view = PlayTournamentView()

	def __call__(self):
		tournament_id = self.view.get_tournament()
		tournament = Tournament.deserialize(tournament_id)
		tournament.play()
		return HomeMenuController

class CreateReportController:
	pass

class EndScreenController:

	def __call__(self):
		print ("Quitter l'application")
