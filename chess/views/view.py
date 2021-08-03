class HomeMenuView:
    """View handling HomeMenuController."""

    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        """Print each key - entry of menu.items()"""
        for key, entry in self.menu.items():
            print(f"{key} : {entry.option}")

    def get_user_choice(self):
        """Return user choice of menu."""
        while True:
            self._display_menu()
            choice = input(">>")
            if choice in self.menu:
                return self.menu[choice]


class CreatePlayerView:
    """View handling CreatePlayerController."""

    def get_player_informations(self, key):
        """Return user's inputs as value for key."""
        value = input(f"{key} ?")
        return value

    def confirm_fields(self, fields):
        """Return True if user confirms informations - False if not."""
        for field in fields:
            print(field)
        confirm = input("Confirm new player ? Press y")
        if confirm == "y":
            return True
        else:
            print("Creation of new player cancelled")
            return False

    def player_saved(self, player):
        """Print confirmation of saving profil of a player in database."""
        print(
            f"Profil de {player.firstname.capitalize()} sauvegardé - ID = {player.id}"
        )
        return None


class CreateTournamentView:
    """View handling CreateTournamentController."""

    def offers_playing_uncompleted(self, uncompleted_dict):
        """Return True if user chooses to play uncompleted tournament - False if not."""
        print("A uncompleted tournament stills remains in database")
        print(f"Name : {uncompleted_dict['name']}")
        print(f"Place : {uncompleted_dict['place']}")
        print(f"Description : {uncompleted_dict['description']}")
        print(
            f"From {uncompleted_dict['starting_day']} to {uncompleted_dict['ending_day']} "
        )
        confirm = input(
            "Play this tournament ? Press y\nIf no, this tournament will be deleted from database"
        )
        if confirm == "y":
            return True
        else:
            print(
                "Tournament uncompleted deleted - Launching of new tournament creation"
            )
            return False

    def get_tournament_informations(self, key):
        """Return user's inputs as value for key."""
        value = input(f"{key} ?")
        return value

    def confirm_fields(self, fields):
        """Return True if user confirms informations - False if not."""
        for field in fields:
            print(field)
        confirm = input("Confirm new tournament ? Press y")
        if confirm == "y":
            return True
        else:
            print("Creation of new tournament cancelled")
            return False

    def add_player_to_tournament(self):
        """Return player's id gave by user."""
        player_id = input("Player ID ?")
        return player_id

    def new_tournament_created(self, new_tournament):
        """Print confirmation of saving tournament in database."""
        print(
            f"{new_tournament.name} is now saved in database - ID = {new_tournament.id}"
        )
        return None


class PlayTournamentView:
    """View handling PlayTournamentController."""

    def confirms_tournament(self, tournament_dict):
        """Return True if user confirms informations and launch playing tournament - False if not."""
        print("Tournament uncompleted :")
        print(f"Name : {tournament_dict['name']}")
        print(f"ID : {tournament_dict['id']}")
        confirm = input("Confirm play tournament ? Press y")
        if confirm == "y":
            return True
        else:
            print("Launching of tournament cancelled")
            return False

    def unfounded_tournament(self):
        """Informs user no uncompleted tournament in database."""
        print("No uncompleted tournament found.")
        confirm = input("Create a new tournament ? Press y")
        if confirm == "y":
            return True
        else:
            print("Back to home menu.")
            return False

    def present_matches(self, round):
        """Print matches of round."""
        print(f"Matches round n°{round.number}")
        for match in round.matches:
            print(match)
        print("\n")
        return None

    def play_match(self, match):
        """Return input of user 0 or 1 or 2."""
        winner = input(
            f"Who is the winner : 1- {match.player_1.firstname} | 2- {match.player_2.firstname} | 0- Draw ?"
        )
        return winner

    def update_classment(self, players):
        """Print each player of players."""
        print("\nClassement actuel :")
        for player in players:
            print(
                f"{player.firstname.capitalize()} avec {player.tournament_point} points - Ranking = {player.ranking}"
            )
        print("\n")
        return None

    def waiting_screen(self):
        """Waiting screen."""
        input(
            "--- Waiting screen --- Press any to finish Round and update scores --- Waiting screen ---"
        )
        return None

    def get_new_ranking(self, player):
        """Return new ranking of player."""
        print(f"{player.firstname.capitalize()} {player.lastname.capitalize()}")
        print(f"Player ID : {player.id}")
        print(f"Actual ranking : {player.ranking}")
        new_rank = input("New rank ? >>")
        return new_rank


class UpdateRankingView:
    """View handling UpdateRankingController."""

    def get_player_id(self):
        """Return ID entered by user."""
        print("Enter player ID")
        player_id = input(">>")
        return player_id

    def get_new_ranking(self, player):
        """Return new ranking of player."""
        print(f"{player.firstname.capitalize()} {player.lastname.capitalize()}")
        print(f"Player ID : {player.id}")
        print(f"Actual ranking : {player.ranking}")
        new_rank = input("New rank ? >>")
        return new_rank


class CreateReportMenuView:
    """View handling CreateReportMenuController."""

    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        """Print each key - entry of menu.items()"""
        for key, entry in self.menu.items():
            print(f"{key} : {entry.option}")
        return None

    def get_user_choice(self):
        """Return user choice of menu."""
        while True:
            self._display_menu()
            choice = input(">>")
            if choice in self.menu:
                return self.menu[choice]


class CreateReportView:
    """View handling creating reports controllers."""

    def get_report_criterion(self):
        """Return reference of criterion of research choosed by user."""
        print("Report by 1- Alphabetic order | 2- Ranking")
        criterion = input(">>")
        return criterion

    def presents_players_report(self, report):
        """Print items of players report via list comprehension - Return None."""
        for item in report:
            print(f"{item['firstname']} {item['lastname']}")
            print(f"ID : {item['id']})- Ranking : {item['ranking']}")
            print("")
        return None

    def presents_tournaments_report(self, report):
        """Print items of tournaments report via list comprehension - Return None."""
        for item in report:
            print(f"Tournament : {item['name']}")
            print(
                f"Place : {item['place']} - From {item['starting_day']} to {item['ending_day']}"
            )
            print(f"Time-control : {item['time_control']}")
            print(f"{item['description']}")
            print("")
        return None

    def get_id(self):
        """Return an integer via user's input."""
        print("ID ?")
        choosen_id = input(">>")
        return choosen_id

    def presents_rounds_report(self, report):
        """Print items of tournament's rounds report via list comprehension - Return None."""
        for item in report:
            print(f"Name : {item['name']}")
            print(f"Number : {item['number']}")
            print(f"From {item['date_time_start']} to {item['date_time_end']}")
            print(f"Matches : {item['matches']}")
        return None

    def presents_matches_report(self, report):
        """Print items of tournament's matches report via list comprehension - Return None."""
        for item in report:
            print(item)
        return None


class EndScreenView:
    """View handling EndScreenController - Return None."""

    def ends(self):
        """Print leaving screen."""
        print("Leaving application")
        return None
