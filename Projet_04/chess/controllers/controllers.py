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
		new_player_infos = []
		new_player_keys = Player.list_attributes()
		for key in new_player_keys:
			value = self.view.get_player_informations(key)
			while Player.is_clean(key, value) is False:
				self.view.invalid_value()
				value = self.view.get_player_informations(key)
			else:
				new_player_infos.append(value)
		player_fields= []
		for field in zip(new_player_keys, new_player_infos):
			player_fields.append(field)
		if self.view.confirm_fields(player_fields):
			new_player = Player(*new_player_infos)
			new_player.save(new_player)
			self.view.player_saved(new_player)
		return HomeMenuController

class CreateTournamentController:
	
	def __init__(self):
		self.view = CreateTournamentView()

	def __call__(self):
		new_tournament_attributes = self.view.get_tournament_informations()
		new_tournament = Tournament(*new_tournament_attributes)
		while len(new_tournament.players) != new_tournament.number_of_players:
			new_tournament.add_player(self.view.add_player_to_tournament())
		new_tournament.save(new_tournament)
		self.view.new_tournament_created(new_tournament)
		return HomeMenuController

class PlayTournamentController:

	def __init__(self):
		self.view = PlayTournamentView()

	def __call__(self):
		tournament_id = self.view.get_tournament()
		tournament = Tournament.deserialize(tournament_id)
		while tournament.current_round != tournament.number_of_rounds:
			if tournament.current_round == 0:
				round = tournament.organize_first_round()
				self.view.update_classment(tournament.players)
				self.view.present_matches(round)
				for match in round.matches:
					result = self.view.play_match(match)
					match.winner_is(result)
				tournament.sort_players()
				tournament.end_round_update(tournament)
			else :
				round = tournament.organize_next_round()
				self.view.update_classment(tournament.players)
				self.view.present_matches(round)
				for match in round.matches:
					result = self.view.play_match(match)
					match.winner_is(result)
				self.view.update_classment(tournament.sort_players())
				tournament.end_round_update(tournament)
		return HomeMenuController

class CreateReportController:
	pass

class EndScreenController:

	def __call__(self):
		print ("Quitter l'application")