from models.player import Player
# from models.tournament import Tournament
# from models.match import Match
from utils.menus import Menu
from views.view import *
from tinydb import TinyDB, Query

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
		print (new_player)

class CreateTournamentController:
	
	def __call__(self):
		print ("Contrôleur de création de tournoi")

class CreateReportController:
	pass

class EndScreenController:

	def __call__(self):
		print ("Quitter l'application")
