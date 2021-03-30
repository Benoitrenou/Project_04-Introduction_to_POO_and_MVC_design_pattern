import requests
from bs4 import BeautifulSoup
import csv
import shutil
from script_fonctions import getbookdata
from script_fonctions import downloadimage
from script_fonctions import getresponseandsoup 
import re #traiter regular expression

url = input ('URL de votre livre : ')

#envoyer requête - si réponse ok-200 exécuter fonctions   
response = requests.get(url) 
if response.ok :
	getbookdata (url)  
	#via beautifulsoup traite et parse code HTML de l'URL - Extrait données requises 
	downloadimage(url) 
	#Requête URL de l'image - si 200 télécharge l'image - sinon print message d'erreur

#message erreur si problème dans URL
else : 
	print (response)
	print ('Erreur : révisez URL du livre ou votre connexion')	

with open(f"livre-{title}.csv", "w", encoding="utf-8") as outf: 
#ouverture en dynamique pour fermer automatiquement à la sortie de l'indentation
	spamwriter = csv.writer(outf, delimiter=";")
	outf.write("Titre;UPC;Catégorie;Description;Prix HT en £;Prix TTC en £;Articles en stock;URL Image;Note sur 5;URL article\n")
	#Ligne en-tête 
	outf.write(title+ ";"+ UPC+ ";"+ CATEG+ ";"+ DESC+ ";"+ prixHT+ ";"+ prixTTC+ ";"+ stock+ ";"+ image_url+ ";"+ note+ ";"+ url+ "\n")
	print (f'Données {title} téléchargées et disponibles')
	#Ecriture données extraites via fonction getbookdata 
