import requests
from bs4 import BeautifulSoup
import re #traiter regular expression

url = input ('URL de votre livre : ')

response = requests.get(url) 
#envoyer requête - si réponse ok-200 :  
if response.ok : 
	soup = BeautifulSoup (response.text, features = 'lxml')
	#BeautifulSoup renvoie en réponse code HTML format text en utilisant parser souhaité - 'lxml'
	#soup.find utilise BS pour trouver balises correspondantes dans code HTML et extraire donnée souhaitée
	title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text
	
	upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
	
	UPC = upc[0].text
	prixHT = upc[2].text.replace("Â", "").replace("£", "")
	prixTTC = upc[3].text.replace("Â", "").replace("£", "")
	
	stock = re.sub("[^0-9]", "", soup.find("p", class_="instock availability").text)

	catégorie = soup.find("ul", {"class": "breadcrumb"}).find_all("li")
	CATEG = catégorie[2].text.replace("\n", "")

	description = soup.find("article", {"class": "product_page"}).find_all("p")
	DESC = description[3].text.replace(";", ",")

	image = soup.find("img")
	image_url = f'http://books.toscrape.com/{image["src"]}'

	rating = soup.find("p", class_=re.compile("star-rating")).get("class")[1]
	rating_dic = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
	note = rating_dic[rating]

	print (f'{title}, {UPC}')
	#print pour vérifier bonne exécution

#message erreur si problème dans URL
else : 
	print (response)
	print ('Erreur : révisez URL ou connexion')	