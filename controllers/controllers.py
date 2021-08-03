from datetime import datetime
from models.player import Player, PlayerManager
from models.tournament import Tournament, TournamentManager
from utils.menus import Menu
import views.view as view
from utils.exceptions import CustomValueError, CustomAssertionError


class ApplicationController:
    """Main controller of application - Runs others controllers."""

    def __init__(self):
        self.controller = None

    def start(self):
        """Initiate boucle of controllers."""
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    """Controller of home menu."""

    def __init__(self):
        self.menu = Menu()
        self.view = view.HomeMenuView(self.menu)

    def __call__(self):
        """Present home menu - Return user choice handler."""
        self.menu.add("auto", "Create a player", CreatePlayerController)
        self.menu.add("auto", "Create a tournament", CreateTournamentController)
        self.menu.add("auto", "Play a tournament", PlayTournamentController)
        self.menu.add("auto", "Update a player's ranking", UpdateRankingController)
        self.menu.add("auto", "Create a report", CreateReportMenuController)
        self.menu.add("q", "Leave the application", EndScreenController)
        user_choice = self.view.get_user_choice()
        return user_choice.handler


class CreatePlayerController:
    """Controller handling instanciation of Player."""

    def __init__(self):
        self.view = view.CreatePlayerView()
        self.manager = PlayerManager()

    def __call__(self):
        """Manage creation of new player with user's inputs - Return HomeMenuController."""
        new_player_infos = []
        new_player_keys = Player.list_attributes()
        for key in new_player_keys:
            value = self.view.get_player_informations(key)
            while self.clean_attributes_infos(key, value) is False:
                value = self.view.get_player_informations(key)
            else:
                new_player_infos.append(value)
        player_fields = []
        for field in zip(new_player_keys, new_player_infos):
            player_fields.append(field)
        if self.view.confirm_fields(player_fields):
            new_player = Player(*new_player_infos)
            self.manager.save(new_player)
            self.view.player_saved(new_player)
        return HomeMenuController

    def clean_attributes_infos(self, key, value):
        """Validate format attributes for Player instanciation."""
        if key == "Birthday DD/MM/YYYY":
            try:
                value == datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                CustomValueError("This format of date is not valid - Please follow format DD/MM/YYY")
                return False
        elif key == "Sex M/F":
            try:
                assert value.capitalize() in Player.SEX_POSSIBLE
            except AssertionError:
                CustomAssertionError("This is not a valid sex - Please enter a valid answer M/F")
                return False
        elif key == "Ranking - Positive Integers":
            try:
                int(value)
            except ValueError:
                CustomValueError("This is not a valid rank - Please enter a positive integers")
                return False
            try:
                assert int(value) > 0
            except AssertionError:
                CustomAssertionError("This is not a valid rank - Please enter a positive integers")
                return False
        else:
            return True


class CreateTournamentController:
    """Controller handling instanciation of Tournament."""

    def __init__(self):
        self.view = view.CreateTournamentView()
        self.tournament_manager = TournamentManager()
        self.player_manager = PlayerManager()

    def __call__(self):
        """Manage creation of new tournament with user's inputs - Return HomeMenuController."""
        uncompleted_dict = self.tournament_manager.find_uncompleted()
        if uncompleted_dict is not None:
            if self.view.offers_playing_uncompleted(uncompleted_dict):
                return PlayTournamentController
            else:
                self.tournament_manager.remove_tournament(uncompleted_dict["id"])
        new_tournament_infos = []
        new_tournament_keys = Tournament.list_attributes()
        for key in new_tournament_keys:
            value = self.view.get_tournament_informations(key)
            while self.clean_attributes_infos(key, value) is False:
                value = self.view.get_tournament_informations(key)
            else:
                new_tournament_infos.append(value)
        tournament_fields = []
        for field in zip(new_tournament_keys, new_tournament_infos):
            tournament_fields.append(field)
        if self.view.confirm_fields(tournament_fields):
            new_tournament = Tournament(*new_tournament_infos)
            while len(new_tournament.players) != new_tournament.number_of_players:
                new_player_id = self.view.add_player_to_tournament()
                while self.check_new_player_id(new_player_id) is False:
                    new_player_id = self.view.add_player_to_tournament()
                new_tournament.add_player(new_player_id)
            self.tournament_manager.save(new_tournament)
            self.view.new_tournament_created(new_tournament)
        return HomeMenuController

    def clean_attributes_infos(self, key, value):
        """Validate format of attributes for Tournament instanciation."""
        if key == "Time_control 1-Bullet | 2-Blitz | 3-Coup Rapide":
            try:
                int(value)
            except ValueError:
                CustomValueError("This is not a valid answer - Please choose 1 - 2 or 3")
                return False
            try:
                assert int(value) in [1, 2, 3]
            except AssertionError:
                CustomAssertionError("This is not a valid answer - Please choose 1 - 2 or 3")
                return False
        if key == "Starting_day DD/MM/YYYY" or key == "Ending_day DD/MM/YYYY":
            try:
                value == datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                CustomValueError("This format of date is not valid - Please follow format DD/MM/YYY")
                return False

    def check_new_player_id(self, new_player_id):
        """Verifies if new player ID is valid and exists in database."""
        try:
            int(new_player_id)
        except ValueError:
            CustomValueError("This is not a valid ID")
            return False
        try:
            assert self.player_manager.search_by_id(new_player_id) is not None
        except AssertionError:
            CustomAssertionError("This ID is not assigned")
            return False
        return True


class PlayTournamentController:
    """Controller handling course of a Tournament."""

    def __init__(self):
        self.view = view.PlayTournamentView()
        self.tournament_manager = TournamentManager()
        self.player_manager = PlayerManager()

    def __call__(self):
        """Manage steps of being played tournament."""
        tournament_dict = self.tournament_manager.find_uncompleted()
        if tournament_dict is None:
            if self.view.unfounded_tournament():
                return CreateTournamentController
            else:
                return HomeMenuController
        if self.view.confirms_tournament(tournament_dict):
            tournament = Tournament.deserialize(tournament_dict["id"])
        else:
            return HomeMenuController
        while tournament.current_round != tournament.number_of_rounds:
            if tournament.current_round == 0:
                round = tournament.organize_first_round()
            else:
                round = tournament.organize_next_round()
            round.starts()
            self.view.update_classment(tournament.players)
            self.view.present_matches(round)
            self.view.waiting_screen()
            round.ends()
            for match in round.matches:
                result = self.view.play_match(match)
                while self.check_result_validity(result) is False:
                    result = self.view.play_match(match)
                match.winner_is(int(result))
            self.view.update_classment(tournament.sort_players())
            if tournament.current_round == tournament.number_of_rounds:
                tournament.completed = tournament.is_finished()
                for player in tournament.players:
                    new_rank = self.view.get_new_ranking(player)
                    while self.check_rank_validity(new_rank) is False:
                        new_rank = self.view.get_new_ranking(player)
                    self.player_manager.update_ranking(player.id, new_rank)
            self.tournament_manager.saves_update(tournament)
        return HomeMenuController

    def check_rank_validity(self, rank):
        """Verifies if rank is a positive integers - Returns False if not."""
        try:
            int(rank)
        except ValueError:
            CustomValueError("This is not a valid rank - Please enter a positive integers")
            return False
        try:
            assert int(rank) > 0
        except AssertionError:
            CustomAssertionError("This is not a valid rank - Please enter a positive integers")
            return False
        return True

    def check_result_validity(self, result):
        """Verifies if result is valid - Returns False if not."""
        try:
            int(result)
        except ValueError:
            CustomValueError("This is not a valid answer - Please choose winner 1-2 or 0 for draw")
            return False
        try:
            assert int(result) in [0, 1, 2]
        except AssertionError:
            CustomAssertionError("This is not a valid answer - Please choose winner 1-2 or 0 for draw")
            return False
        return True


class UpdateRankingController:
    """Controller managing update of a Player's ranking."""

    def __init__(self):
        self.view = view.UpdateRankingView()
        self.manager = PlayerManager()

    def __call__(self):
        """Manages updating of player's rank with user's inputs - Return HomeMenuController."""
        player_id = self.view.get_player_id()
        while self.check_id_validity(player_id) is False:
            player_id = self.view.get_player_id()
        player = Player.deserialize(self.manager.search_by_id(player_id))
        new_rank = self.view.get_new_ranking(player)
        while self.check_rank_validity(new_rank) is False:
            new_rank = self.view.get_new_ranking(player)
        self.manager.update_ranking(player.id, new_rank)
        return HomeMenuController

    def check_id_validity(self, player_id):
        """Verifies if player ID is valid and exists in database."""
        try:
            int(player_id)
        except ValueError:
            CustomValueError("This is not a valid ID - ID must be a positive integers")
            return False
        try:
            assert self.manager.search_by_id(player_id) is not None
        except AssertionError:
            CustomAssertionError("This ID is not assigned in database")
            return False
        return True

    def check_rank_validity(self, rank):
        """Verifies if rank is a positive integers - Returns False if not."""
        try:
            int(rank)
        except ValueError:
            CustomValueError("This is not a valid rank - Please enter a positive integers")
            return False
        try:
            assert int(rank) > 0
        except AssertionError:
            CustomAssertionError("This is not a valid rank - Please enter a positive integers")
            return False
        return True


class CreateReportMenuController:
    """Main menu to create report."""

    def __init__(self):
        self.menu = Menu()
        self.view = view.CreateReportMenuView(self.menu)

    def __call__(self):
        """Present reports menu - Return user choice handler."""
        self.menu.add("auto", "Report of all players", AllPlayersReportController)
        self.menu.add("auto", "Report of all tournaments", AllTournamentsReportController)
        self.menu.add("auto", "Report of players of a tournament",TournamentPlayersReportController)
        self.menu.add("auto", "Report of rounds of a tournament", TournamentRoundsReportController)
        self.menu.add("auto","Report of matchs of a tournament",TournamentMatchesReportController)
        self.menu.add("q", "Back to Home Menu", HomeMenuController)
        user_choice = self.view.get_user_choice()
        return user_choice.handler


class AllPlayersReportController:
    """Controller managing all players report creation."""

    def __init__(self):
        self.view = view.CreateReportView()
        self.manager = PlayerManager()

    def __call__(self):
        """Manage presentation of all players report - Return CreateReportMenuController."""
        results = self.manager.all_players_report()
        criterion = self.view.get_report_criterion()
        while self.check_criterion_validity(criterion) is False:
            criterion = self.view.get_report_criterion()
        if int(criterion) == 1:
            results.sort(key=lambda x: (x["lastname"], x["firstname"]))
        if int(criterion) == 2:
            results.sort(key=lambda x: (x["ranking"]), reverse=True)
        self.view.presents_players_report(results)
        return CreateReportMenuController

    def check_criterion_validity(self, criterion):
        """Verify validity of criterion inputted by user."""
        try:
            int(criterion)
        except ValueError:
            CustomValueError("Invalid criterion - Please choose 1 or 2")
            return False
        try:
            assert int(criterion) in [1, 2]
        except AssertionError:
            CustomAssertionError("Invalid criterion - Please choose 1 or 2")
            return False
        return True


class AllTournamentsReportController:
    """Controller managing all tournaments report creation."""

    def __init__(self):
        self.view = view.CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        """Manage presentation of all tournaments report - Return CreateReportMenuController."""
        results = self.manager.tournaments_report()
        self.view.presents_tournaments_report(results)
        return CreateReportMenuController


class TournamentPlayersReportController:
    """Controller managing a tournament's players report creation."""

    def __init__(self):
        self.view = view.CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        """Manage presentation of a tournament's players report - Return CreateReportMenuController."""
        tournament_id = self.view.get_id()
        results = self.manager.tournament_players_report(tournament_id)
        criterion = self.view.get_report_criterion()
        while self.check_criterion_validity(criterion) is False:
            criterion = self.view.get_report_criterion()
        if int(criterion) == 1:
            results.sort(key=lambda x: (x["lastname"], x["firstname"]))
        if int(criterion) == 2:
            results.sort(key=lambda x: (x["ranking"]), reverse=True)
        self.view.presents_players_report(results)
        return CreateReportMenuController

    def check_criterion_validity(self, criterion):
        """Verify validity of criterion inputted by user."""
        try:
            int(criterion)
        except ValueError:
            CustomValueError("Invalid criterion - Please choose 1 or 2")
            return False
        try:
            assert int(criterion) in [1, 2]
        except AssertionError:
            CustomAssertionError("Invalid criterion - Please choose 1 or 2")
            return False
        return True


class TournamentRoundsReportController:
    """Controller managing tournament's rounds report creation."""

    def __init__(self):
        self.view = view.CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        """Manage presentation of a tournament's rounds report - Return CreateReportMenuController."""
        tournament_id = self.view.get_id()
        results = self.manager.tournament_rounds_report(tournament_id)
        self.view.presents_rounds_report(results)
        return CreateReportMenuController


class TournamentMatchesReportController:
    """Controller managing a tournament's matches report creation."""

    def __init__(self):
        self.view = view.CreateReportView()
        self.manager = TournamentManager()

    def __call__(self):
        """Manage presentation of a tournament's matches report - Return CreateReportMenuController."""
        tournament_id = self.view.get_id()
        results = self.manager.tournament_matches_report(tournament_id)
        self.view.presents_matches_report(results)
        return CreateReportMenuController


class EndScreenController:
    """Controller managing end of application."""

    def __init__(self):
        self.view = view.EndScreenView()

    def __call__(self):
        """Manage end of application - Return None."""
        self.view.ends()
        return None
