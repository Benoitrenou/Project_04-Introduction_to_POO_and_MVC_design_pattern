The objective in the scenario of this project is to implement a chess tournament result tracking tool that follows the "Swiss round" format in a simplified version
The tool allows to:
- Register players to the tournament
- Register in the database the first entrants
- Organize the matches according to the players' ranking and results
- Follow the results of the games and the tournament

Objectives of the project:
- Learn object-oriented programming
- Set up a simple database via TinyDB
- Organize an application following the Model-View-Controller pattern

First, you can clone the repository:

    $ git clone https://github.com/Benoitrenou/projet_04.git    

# I. Installation of virtual environment 

From your terminal, use the following commands

## Creation of virtual environment: 

### With Linux/ MAC OS

    $ python -m venv <environment_name>
    example : python -m venv env_chess
    
### With Windows:
    
    $ virtualenv <environment_name>
    exemple : virtualenv env_chess 
    
## Activation of virtual environment : 

### With Linux / MAC OS:

    $ source <environment_name>/bin/activate
    exemple : source env_chess/bin/activate
   
### With Windows:

    $ source <environment_name>/Scripts/activate
    exemple : source env_chess/Scripts/activate
    
## Installation of packages : 

    $ pip install -r requirements.txt

# II. Use of script

To launch the application, in the terminal use the command:

    $ python main.py

From the main menu, you can now:
    - Create a player into the database
    - Create a tournament into the database
    - Play a tournament - If no tournament is found in database, the script will propose you to create a new one
    - Update a player's ranking
    - Create a report
        Many reports are availables: all players by ranking or alphabetic order, all tournaments, details of players-rounds-matchs of tournament, etc. Feel free to search of !

Just follow the instructions of the terminal for each of your choices, and don't forget to respect format in each of your response

    example : date of tournament must be format DD/MM/YYYY

# III. Generate a flake8 report

To generate a new flake8 report, from the terminal enter the command

    $ flake8 C:/path_to_local_repository