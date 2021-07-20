from models.player import Player, PlayerManager
from models.tournament import Tournament, TournamentManager
from utils.menus import Menu
from views.view import *


class ApplicationController:
    def __init__(self):
        self.controller = None

    def start(self):
        """Initiate boucle of controllers."""
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Create a player", CreatePlayerController)
        self.menu.add("auto", "Create a tournament", CreateTournamentController)
        self.menu.add("auto", "Play a tournament", PlayTournamentController)
        self.menu.add("auto", "Update a player's ranking", UpdateRankingController)
        self.menu.add("auto", "Create a report", CreateReportMenuController)
        self.menu.add("q", "Leave the application", EndScreenController)
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
            while Player.clean_attributes_infos(key, value) is False:
                self.view.invalid_value()
                value = self.view.get_player_informations(key)
            else:
                new_player_infos.append(value)
        player_fields = []
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
        new_tournament_infos = []
        new_tournament_keys = Tournament.list_attributes()
        for key in new_tournament_keys:
            value = self.view.get_tournament_informations(key)
            while Tournament.clean_attributes_infos(key, value) is False:
                self.view.invalid_value()
                value = self.view.get_tournament_informations(key)
            else:
                new_tournament_infos.append(value)
        tournament_fields = []
        for field in zip(new_tournament_keys, new_tournament_infos):
            tournament_fields.append(field)
        if self.view.confirm_fields(tournament_fields):
            new_tournament = Tournament(*new_tournament_infos)
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
                round.starts()
                # tournament.saves_update(tournament)
                self.view.update_classment(tournament.players)
                self.view.present_matches(round)
                self.view.waiting_screen()
                round.ends()
                for match in round.matches:
                    result = self.view.play_match(match)
                    match.winner_is(result)
                tournament.sort_players()
                tournament.saves_update(tournament)
            else:
                round = tournament.organize_next_round()
                round.starts()
                # tournament.saves_update(tournament)
                self.view.update_classment(tournament.players)
                self.view.present_matches(round)
                self.view.waiting_screen()
                round.ends()
                for match in round.matches:
                    result = self.view.play_match(match)
                    match.winner_is(result)
                self.view.update_classment(tournament.sort_players())
                if tournament.current_round == tournament.number_of_rounds:
                    for player in tournament.players:
                        new_rank = self.view.get_new_ranking(player)
                        while (
                            Player.clean_attributes_infos("ranking", new_rank) is False
                        ):
                            new_rank = self.view.get_new_ranking(player)
                        player.update_ranking(player.id, new_rank)
                tournament.saves_update(tournament)
        return HomeMenuController


class UpdateRankingController:
    def __init__(self):
        self.view = UpdateRankingView()

    def __call__(self):
        player_id = self.view.get_player_id()
        try:
            int(player_id)
        except ValueError:
            return UpdateRankingController
        player = Player.deserialize(PlayerManager.search_by_id(player_id))
        new_rank = self.view.get_new_ranking(player)
        while Player.clean_attributes_infos("ranking", new_rank) is False:
            new_rank = self.view.get_new_ranking(player)
        player.update_ranking(player.id, new_rank)
        return HomeMenuController


class CreateReportMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = CreateReportMenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Report of all players", AllPlayersReportController)
        self.menu.add("auto", "Report of all tournaments", AllTournamentsReportController)
        self.menu.add("auto", "Report of players of a tournament", TournamentPlayersReportController)
        self.menu.add("auto", "Report of rounds of a tournament", TournamentRoundsReportController)
        self.menu.add("auto", "Report of matchs of a tournament", TournamentMatchesReportController)
        self.menu.add("q", "Back to Home Menu", HomeMenuController)
        user_choice = self.view.get_user_choice()
        return user_choice.handler


class AllPlayersReportController:
    def __init__(self):
        self.view = CreateReportView()
        self.manager = PlayerManager()

    def __call__(self):
        results = self.manager.all_players_report()
        criterion = self.view.get_report_criterion()
        try:
            int(criterion)
            if int(criterion) not in [1, 2]:
                self.view.invalid_value()
                return CreateReportMenuController
        except ValueError:
            self.view.invalid_value()
            return CreateReportMenuController
        if int(criterion) == 1:
            results.sort(key=lambda i: (i["lastname"], i["firstname"]))
        if int(criterion) == 2:
            results.sort(key=lambda i: (i["ranking"]), reverse=True)
        self.view.presents_players_report(results)
        return HomeMenuController

class AllTournamentsReportController:
    def __init__(self):
        self.view = CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        results = self.manager.tournaments_report()
        self.view.presents_tournaments_report(results)
        return HomeMenuController

class TournamentPlayersReportController:
    def __init__(self):
        self.view = CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        tournament_id = self.view.get_id()
        results = self.manager.tournament_players_report(tournament_id)
        criterion = self.view.get_report_criterion()
        try:
            int(criterion)
            if int(criterion) not in [1, 2]:
                self.view.invalid_value()
                return CreateReportMenuController
        except ValueError:
            self.view.invalid_value()
            return CreateReportMenuController
        if int(criterion) == 1:
            results.sort(key=lambda i: (i["lastname"], i["firstname"]))
        if int(criterion) == 2:
            results.sort(key=lambda i: (i["ranking"]), reverse=True)
        self.view.presents_players_report(results)
        return HomeMenuController

class TournamentRoundsReportController:
    def __init__(self):
        self.view = CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        tournament_id = self.view.get_id()
        results = self.manager.tournament_rounds_report(tournament_id)
        self.view.presents_rounds_report(results)
        return HomeMenuController

class TournamentMatchesReportController:
    def __init__(self):
        self.view = CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        tournament_id = self.view.get_id()
        results = self.manager.tournament_matches_report(tournament_id)
        self.view.presents_matches_report(results)
        return HomeMenuController

class EndScreenController:
    def __call__(self):
        print("Quitter l'application")
