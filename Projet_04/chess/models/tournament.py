from itertools import repeat
from datetime import datetime
from .round import Round
from .player import Player
from .match import Match
from tinydb import TinyDB, Query

db = TinyDB("db.json", indent=4)
tournaments_table = db.table("tournaments")
# tournaments_table.truncate()
players_table = db.table("players")
query = Query()


class TournamentManager:
    def save(self, tournament, table=tournaments_table):
        """Tournament's saving method"""
        tournament.id = table.insert(tournament.serialize())
        tournaments_table.update({"id": tournament.id}, query.name == tournament.name)

    def saves_update(
        self,
        tournament,
        tournaments_table=tournaments_table,
        players_table=players_table,
    ):
        """Tournament's database updating method"""
        updated_rounds = [round.serialize() for round in tournament.rounds]
        updated_matches = [
            match.serialize() for match in tournament.matches_already_played
        ]
        tournaments_table.update(
            {"rounds": updated_rounds}, query.name == tournament.name
        )
        tournaments_table.update(
            {"matches_already_played": updated_matches}, query.name == tournament.name
        )
        tournaments_table.update(
            {"current_round": tournament.current_round}, query.name == tournament.name
        )
        for player in tournament.players:
            players_table.update(
                {"tournament_point": player.tournament_point},
                query.firstname == player.firstname,
            )


class Tournament(TournamentManager):

    DEFAULT_NUMBER_OF_PLAYERS = 8
    DEFAULT_NUMBER_OF_ROUNDS = 4
    DEFAULT_TIME_CONTROL = {1:'Bullet', 2:'Blitz', 3:'Coup Rapide'}

    def __init__(
        self, name, place, starting_day, ending_day, time_control, description
    ):
        self.name = name
        self.place = place
        self.starting_day = starting_day
        self.ending_day = ending_day
        self.time_control = time_control
        self.description = description
        self.rounds = []
        self.players = []
        self.matches_already_played = []
        self.current_round = 0
        self.number_of_players = self.DEFAULT_NUMBER_OF_PLAYERS
        self.number_of_rounds = self.DEFAULT_NUMBER_OF_ROUNDS
        # self.is_finished = self.is_finished()

    # def is_finished(self):
    # 	if self.number_of_rounds == self.current_round:
    # 		return True
    # 	else:
    # 		return False

    def add_player(self, ref_joueur, players_table=players_table):
        """Add a player from database with his id to Tournament."""
        self.players.append(
            Player.deserialize(players_table.get(doc_id=float(ref_joueur)))
        )
        for player in self.players:
            player.tournament_point = 0

    def organize_first_round(self):
        """Return first round and his matches"""
        for player in self.players:
            player.tournament_point = 0
        self.current_round += 1
        self.sort_players()
        self.round = Round(f"Round_{str(self.current_round)}", self.current_round)
        self.rounds.append(self.round)
        half_index = int(self.number_of_players / 2)
        players_first_half = self.players[:half_index]
        players_second_half = self.players[half_index:]
        for match in zip(players_first_half, players_second_half):
            match = Match(match[0], match[1])
            self.matches_already_played.append(match)
            self.round.add_match(match)
        return self.round

    def organize_next_round(self):
        """Return others rounds than first one and theirs matches."""
        self.current_round += 1
        self.sort_players()
        self.round = Round(f"Round_{self.current_round}", self.current_round)
        self.rounds.append(self.round)
        round_players = self.players[:]
        while len(round_players) != 0:
            player, *others = round_players
            for match in zip(repeat(player), others):
                match = Match(match[0], match[1])
                if match not in self.matches_already_played:
                    round_players.remove(match.player_1)
                    round_players.remove(match.player_2)
                    self.matches_already_played.append(match)
                    self.round.add_match(match)
                    break
        return self.round

    def sort_players(self):
        """Return tournament.players sorted."""
        self.players = sorted(self.players, reverse=True)
        return self.players

    def serialize(self):
        """Return an instance of Tournament in JSON format written data."""
        players = [player.id for player in self.players]
        rounds = [round.serialize() for round in self.rounds]
        matches = [match.serialize() for match in self.matches_already_played]
        return {
            "name": self.name,
            "place": self.place,
            "starting_day": self.starting_day,
            "ending_day": self.ending_day,
            "time_control": self.time_control,
            "description": self.description,
            "rounds": rounds,
            "players": players,
            "matches_already_played": matches,
            "current_round": self.current_round,
            # "finished": self.is_finished
        }

    @classmethod
    def deserialize(
        cls,
        tournament_id,
        tournaments_table=tournaments_table,
        players_table=players_table,
    ):
        """Return instance of Tournament from JSON format written data."""
        data = tournaments_table.get(doc_id=int(tournament_id))
        tournament = cls(
            name=data["name"],
            place=data["place"],
            starting_day=data["starting_day"],
            ending_day=data["ending_day"],
            time_control=data["time_control"],
            description=data["description"],
        )
        for player_id in data["players"]:
            joueur = Player.deserialize(players_table.get(doc_id=player_id))
            tournament.players.append(joueur)
        for round in data["rounds"]:
            tour = Round.deserialize(round)
            tournament.rounds.append(tour)
        for match in data["matches_already_played"]:
            game = Match.deserialize(match)
            tournament.matches_already_played.append(game)
        tournament.current_round = data["current_round"]
        # tournament.is_finished = data["finished"]
        return tournament

    @classmethod
    def list_attributes(cls):
        """Return a list of attributes required to instance Tournament."""
        return [
            "Name",
            "Place",
            "Starting_day DD/MM/YYYY",
            "Ending_day DD/MM/YYYY",
            "Time_control 1-Bullet | 2-Blitz | 3-Coup Rapide",
            "Description",
        ]

    @classmethod
    def clean_attributes_infos(cls, key, value):
    	"""Validate format of attributes for Tournament instanciation."""
    	if key == "Time_control 1-Bullet | 2-Blitz | 3-Coup Rapide":
    		try :
    			int(value)
	    		if int(value) not in [1, 2, 3]:
	    			return False
	    	except ValueError:
	    		return False
    	if key == "Starting_day DD/MM/YYYY" or key == "Ending_day DD/MM/YYYY":
    		try:
    			value == datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
    		except ValueError:
    			return False