Afin de faire fonctionner ces scripts, veuillez suivre les étapes suivantes

Tout d'abord, clônez en local le dépôt distant

    $ git clone https://github.com/Benoitrenou/projet_04.git    

# I. Installation de l'environnement virtuel 

Si vous êtes sur un OS hors Windows 

Depuis votre terminal de commande, effectuez les commandes suivantes 

## Création de l'environnement virtuel : 

### Sous Linux/ MAC OS

    $ python -m venv <environment_name>
    exemple : python -m venv env_chess 
    
### Sous Windows:
    
    $ virtualenv <environment_name>
    exemple : virtualenv env_chess 
    
## Activation de l'environnement virtuel : 

### Sous Linux / MAC OS:

    $ source <environment_name>/bin/activate
    exemple : source env_chess/bin/activate
   
### Sous Windows:

    $ source <environment_name>/Scripts/activate
    exemple : source env_chess/Scripts/activate
    
## Installation des packages : 

    $ pip install -r requirements.txt

# II. Utilisation du script

Pour lancer le script de l'application depuis le terminal, placez vous dans le dossier chess utilisez la commande : 

    $ python main.py

# III. Générer un rapport flake8

Pour générer un nouveau rapport flake8 depuis le terminal, utilisez la commande : 

    $ flake8 --format=html --htmldir=flake-report

