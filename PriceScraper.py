import requests
from bs4 import BeautifulSoup
import re


# Seite 1 Herr-Strom.de
# Hersteller SolarFabrik 360


# URL aufrufen
URL1 = "https://herr-strom.de/p/balkonkraftwerk-solarfabrik-360-plus-alustaender"


#   BeautifulSoup durchsucht die Seite nach genannten Parameter
#   zum Eingrenzen des gewünschten Outputs.
Produkt1 = "Balkonkraftwerk SolarFabrik 360"
req1 = requests.get(URL1)
soup1 = BeautifulSoup(req1.content, "html.parser")


# Html-Baum nach "Containern" durchsuchen, hier <meta> mit Inhalt: attrs = .. ""
table1 = soup1.find("meta", attrs={'property': 'og:price:amount'})

# weiß nicht mehr genau, warum und woher ich das habe, aber war hier nötig
rows1 = table1.prettify()
# Zahlen aus Zeile extrahieren
Preis1 = re.findall('[0-9]+', rows1)

print(f'Der Preis von {Produkt1} beträgt {Preis1[0]} €')

# Seite 2 Balkonkraftwerk-vertrieb.de
# Hersteller Aleo Solar 300-315 Watt

URL2 = "https://balkonkraftwerk-vertrieb.de/produkt/balkonkraftwerk/"
Produkt2 = "Balkonkraftwerk Mini Aleo Solar 255-265"

req2 = requests.get(URL2)
soup2 = BeautifulSoup(req2.content, "html.parser")

table2 = soup2.find("span", attrs={"woocommerce-Price-amount amount"})
rows2 = table2.prettify()

Preis2 = re.findall('[0-9]+', rows2)

print(f'Der Preis von Balkonkraftwerk Mini Aleo Solar beträgt {Preis2[0]} €')
