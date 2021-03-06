from itertools import repeat
from tinydb import TinyDB, Query
from .round import Round
from .player import Player
from .match import Match


db = TinyDB("db.json", indent=4)
tournaments_table = db.table("tournaments")
players_table = db.table("players")
query = Query()


class TournamentManager:
    """Object managing relationship Tournament-database."""

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
        updated_matches = [match.serialize() for match in tournament.matches_already_played]
        tournaments_table.update({"rounds": updated_rounds}, query.name == tournament.name)
        tournaments_table.update({"matches_already_played": updated_matches}, query.name == tournament.name)
        tournaments_table.update({"current_round": tournament.current_round}, query.name == tournament.name)
        tournaments_table.update({"completed": tournament.completed}, query.name == tournament.name)
        for player in tournament.players:
            players_table.update({"tournament_point": player.tournament_point}, query.firstname == player.firstname)

    def tournaments_report(self, table=tournaments_table):
        """Return a list of all tournaments of database."""
        results = []
        for row in table:
            results.append(row)
        return results

    def tournament_players_report(
        self,
        tournament_id,
        tournaments_table=tournaments_table,
        players_table=players_table,
    ):
        """Return a list of JSON data of players of a tournament."""
        report = []
        players = tournaments_table.get(query.id == int(tournament_id))["players"]
        for player_id in players:
            player = players_table.get(query.id == int(player_id))
            report.append(player)
        return report

    def tournament_rounds_report(self, tournament_id, table=tournaments_table):
        """Return JSON data of Rounds of a Tournament."""
        report = table.get(query.id == int(tournament_id))["rounds"]
        return report

    def tournament_matches_report(self, tournament_id, table=tournaments_table):
        """Return JSON data of Matches of a Tournament."""
        report = table.get(query.id == int(tournament_id))["matches_already_played"]
        return report

    def find_uncompleted(self, table=tournaments_table):
        """Return id of tournament uncompleted."""
        tournament = tournaments_table.get(query.completed == False)
        return tournament

    def remove_tournament(self, tournament_id, table=tournaments_table):
        """Remove tournament by his id from database."""
        table.remove(doc_ids=[tournament_id])
        return None


class Tournament:
    """Object Tournament."""

    DEFAULT_NUMBER_OF_PLAYERS = 8
    DEFAULT_NUMBER_OF_ROUNDS = 4
    DEFAULT_TIME_CONTROL = {1: "Bullet", 2: "Blitz", 3: "Coup Rapide"}

    def __init__(self, name, place, starting_day, ending_day, time_control, description, id=None):
        self.name = name
        self.place = place
        self.starting_day = starting_day
        self.ending_day = ending_day
        self.time_control = self.DEFAULT_TIME_CONTROL[int(time_control)]
        self.description = description
        self.rounds = []
        self.players = []
        self.matches_already_played = []
        self.current_round = 0
        self.number_of_players = self.DEFAULT_NUMBER_OF_PLAYERS
        self.number_of_rounds = self.DEFAULT_NUMBER_OF_ROUNDS
        self.completed = False
        self.id = id

    def is_finished(self):
        """Compare current number number and total rounds number - Return True if equal."""
        return int(self.number_of_rounds) == int(self.current_round)

    def add_player(self, player_id, players_table=players_table):
        """Add a player from database with his id to Tournament."""
        self.players.append(Player.deserialize(players_table.get(doc_id=int(player_id))))
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
        for key, value in self.DEFAULT_TIME_CONTROL.items():
            if self.time_control == value:
                time_control = key
        return {
            "name": self.name,
            "place": self.place,
            "starting_day": self.starting_day,
            "ending_day": self.ending_day,
            "time_control": time_control,
            "description": self.description,
            "rounds": rounds,
            "players": players,
            "matches_already_played": matches,
            "current_round": self.current_round,
            "completed": self.completed,
            "id": self.id,
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
            id=data["id"],
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
        tournament.completed = data["completed"]
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
