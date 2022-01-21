import requests
from bs4 import BeautifulSoup
import re


# Seite 1 Herr-Strom.de
# Hersteller SolarFabrik 360



URL1 = "https://herr-strom.de/p/balkonkraftwerk-solarfabrik-360-plus-alustaender"

# URL aufrufen
Produkt1 = "Balkonkraftwerk SolarFabrik 360"
req1 = requests.get(URL1)
soup1 = BeautifulSoup(req1.content, "html.parser")

#   BeautifulSoup durchsucht die Seite nach genannten Parameter
#   zum Eingrenzen des gewünschten Outputs.

table1 = soup1.find("meta", attrs={'property': 'og:price:amount'})

rows1 = table1.prettify()
Preis1 = re.findall('[0-9]+', rows1) # Zahl auslesen
#print(rows1)
print(f'Der Preis von {Produkt1} beträgt {Preis1[0]} €')

# Seite 2 Balkonkraftwerk-vertrieb.de
#Hersteller Aleo Solar 300-315 Watt

URL2 = "https://balkonkraftwerk-vertrieb.de/produkt/balkonkraftwerk/"
