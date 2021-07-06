from models.player import Player
from models.tournament import Tournament
from models.match import Match
import json
from tinydb import Query
from tinydb import TinyDB

DEFAULT_NUMBER_OF_ROUNDS = 4


def main():
	
	db = TinyDB('db.json', indent=4)
	players_table = db.table('players')
	players_table.truncate()
	tournaments_table = db.table('tournaments')
	tournaments_table.truncate()
	joueur = Query()


	benoit = Player ('benoit','joueur1', '03/03/1991', 'M', 1200)
	charline = Player ('charline', 'joueur2', '05/05/1992', 'F', 900)
	kevin = Player ('kevin', 'joueur3', '07/06/1989', 'M', 1300)
	martin = Player ('martin', 'joueur4', '01/02/1956', 'M', 1250)
	paula = Player ('paula', 'joueur5', '02/05/1983', 'F', 450)
	jean = Player ('jean', 'joueur6', '25/06/1993' , 'M', 700)
	adrien = Player ('adrien', 'joueur7', '12/10/1975', 'M', 1000)
	justine = Player ('justine', 'joueur8', '26/09/1960', 'F', 1600)

	for player in [benoit, charline, kevin, martin, paula, jean, adrien, justine] : 
		player.id = players_table.insert(player.serialize())
		players_table.update({"id" : player.id}, joueur.firstname == player.firstname)
		print (f'{player.firstname} id is {player.id}')

	tournoi = Tournament('tournoi_test')
	while len(tournoi.players) != tournoi.DEFAULT_NUMBER_OF_PLAYERS:
		ref_joueur = input('Référence joueur = ?')
		tournoi.add_player(ref_joueur, players_table)

	while tournoi.current_round < 4:
		tournoi.get_next_round()
		tournoi.get_classment(players_table, joueur)

	tournaments_table.insert(tournoi.serialize())


if __name__ == "__main__":
    main()