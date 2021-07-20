from datetime import datetime
from .match import Match


class Round:
    def __init__(self, name, number):
        self.matches = []
        self.name = name
        self.number = number
        self.date_time_start = None
        self.date_time_end = None

    def starts(self):
        """Define the date_time_start attribute of a round at the moment it is called."""
        self.date_time_start = datetime.now().strftime("%d/%m/%Y_%Hh%M-%Ss")

    def ends(self):
        """Define the date_time_end attribute of a round at the moment it is called."""
        self.date_time_end = datetime.now().strftime("%d/%m/%Y_%Hh%M-%Ss")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def add_match(self, match):
        """Add a match to round.matches."""
        self.matches.append(match)
        return self.matches

    def serialize(self):
        """Return an instance of Round in JSON format written data."""
        matches = [match.serialize() for match in self.matches]
        return {
            "matches": matches,
            "name": self.name,
            "number": self.number,
            "date_time_start": self.date_time_start,
            "date_time_end": self.date_time_end,
        }

    @classmethod
    def deserialize(cls, data):
        """Return instance of Round from JSON format written data."""
        round = cls(name=data["name"], number=data["number"])
        round.date_time_start = data["date_time_start"]
        round.date_time_end = data["date_time_end"]
        for match in data["matches"]:
            game = Match.deserialize(match)
            round.matches.append(game)
        return round
