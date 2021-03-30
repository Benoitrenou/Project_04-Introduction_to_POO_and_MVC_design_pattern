import csv
import re
import shutil
import requests
from bs4 import BeautifulSoup
import script_fonctions

soup = getresponseandsoup("http://books.toscrape.com/index.html")
categories_urls = [x.get("href") for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
categories_urls = categories_urls[1:]
#Extraction urls des catégories dans une liste categories_urls

# Définir catégorie
for y in categories_urls:
	print(f'Catégorie disponibles : {y.replace("catalogue/category/books/", "").replace("/index.html", "")}')
categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"

soup = getresponseandsoup(url)
results = soup.find('form', {'class' : 'form-horizontal'}).find('strong').text
print (results)