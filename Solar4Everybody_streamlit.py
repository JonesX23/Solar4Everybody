import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt

def gui_version_1():
    st.set_page_config(layout="wide")
    st.title("Solar4Everybody")
    st.subheader(
        "Du interessierst dich dafür, ob sich ein Balkonkraftwerk auf deinem Balkon lohnt? Super, dann bist du hier genau richtig. Wir leiten dich Schritt für Schritt durch:")

    # 1. Schritt: Liegt der Balkon zur Südseite?
    st.write("""  # 1. Schritt""")
    col1, col2 = st.columns([1, 3])
    with col1:
        # st.image("Kompass.jpeg", width= 150)
        pass
    with col2:
        kompassgrad = st.number_input(
            'In diesem Schritt wollen wir überprüfen, zu welcher Seite (Nord,Ost,Süd oder West) dein Balkon liegt. Nutze hierfür am besten dein Handy und eine geeignete Kompass App. Richte dein Handy so aus, dass du die Himmelsrichtung vom Balkon ablesen kannst.'''
            'Welche Gradzahl zeigt dein Handy an? Bitte trage diese Zahl in das Feld ein.', min_value=0, max_value=360, value=180)
        if 360 >= kompassgrad >= 0:
            if 225 >= kompassgrad >= 125:
                st.write('Super, dein Balkon liegt auf der Südseite. Geh weiter zu Schritt 2!')
            elif kompassgrad == 0:
                st.write('Gib hier bitte deine Gradzahl an.')
            else:
                st.write('Mh, dein Balkon ist nicht so gut geeignet für ein Balkonkraftwerk')
        else:
            st.write('Oh, bist du dir sicher, dass du die richtige Gradzahl eingegeben hast?')

    # 2. Schritt: Platz auf dem Balkon


    if 225 >= kompassgrad >= 125:
        st.write("""  # 2. Schritt""")
        VerfügbarerPLatz = st.selectbox(
            'Wir haben für dich ein Balkonkraftwerk herausgesucht.'
            '(Disclaimer: Nur ein Beispielmodul #nichtgesponsert)'
            'Das Modul hat die folgenden Maße:  1755 x 1038x 35 mm.'

            ' Hast du so viel freien Platz auf dem Balkon?',
            ('Ja', 'Nein'), index=0)
        if VerfügbarerPLatz == 'Ja':
            st.write('Wunderbar, dann geh direkt zu Schritt 3!')
        else:
            st.write('Tut uns leid, dann kommt für dich "unser" Balkonkraftwerk nicht in Frage')

        # 3. Schritt: Vorstellung des Panels

        if VerfügbarerPLatz == 'Ja':
            col3, col4 = st.columns([1,2])
            with col3:
                st.write("""  # 3. Schritt""")
                st.write(
                    "Gut, dann wollen wir dir einmal das Balkonkraftwerk vorstellen, welches wir für dich herausgesucht haben.")
                URL1 = "https://herr-strom.de/p/balkonkraftwerk-solarfabrik-360-plus-alustaender"
                Produkt1 = "Balkonkraftwerk SolarFabrik 360"
                req1 = requests.get(URL1)
                soup1 = BeautifulSoup(req1.content, "html.parser")
                table1 = soup1.find("meta", attrs={'property': 'og:price:amount'})
                rows1 = table1.prettify()
                preis_solarpanel = re.findall('[0-9]+', rows1)
                st.write(f'Der Preis von {Produkt1} beträgt {preis_solarpanel[0]} €')
            with col4:
                # add another column to the right of the info
                x1 = (soup1.find("div", attrs={"class": "product-addition-content"}).find_all("li"))
                child = x1[5].get_text()

                # Webscraping strompreis
                URL_electricity = "https://www.stromauskunft.de/strompreise/"
                req2 = requests.get(URL_electricity)
                soup2 = BeautifulSoup(req2.content, "html.parser")
                strom_table = soup2.find("table", attrs={"class": "table table-condensend table-hover table-striped "
                                                                   "table-sm"})
                strom_table_data = strom_table.tbody.find_all("td")
                strom_table_data_price = strom_table_data[1].get_text()
                strom_table_data_price = (strom_table_data_price[0:5])
                strom_table_data_price = float(strom_table_data_price.replace(",", "."))/100
                current_kwh_price = float("{:.3f}".format(strom_table_data_price))
                watt_integer = int(child[0:3])
                max_earnings_per_years = watt_integer*current_kwh_price
                timepoint_amortisierung = (int(preis_solarpanel[0]))/max_earnings_per_years
                col4.subheader("Amortisierung")
                col4.write(f'Die Amortisierung ist berechnet anhand des aktuellen Strompreises {current_kwh_price} €. '
                           f'Hiernach wuerde sich ein Balkonkraftwerk nach {("%.2f" % timepoint_amortisierung)} Jahren amortisieren')
                berechnungszeitraum_Jahre = 11
                plt.figure(figsize=(3, 3))
                plt.plot((np.linspace(int(preis_solarpanel[0]) * -1,
                                      (int(preis_solarpanel[0]) * -1) + (int(max_earnings_per_years) * 10),
                                      berechnungszeitraum_Jahre)), color="blue",linewidth=0.5)
                plt.axhline(0, xmax=(int(preis_solarpanel[0]) / (int(max_earnings_per_years) * 10)), color='black',
                            linestyle='dashed', linewidth=0.5)
                plt.axvline(timepoint_amortisierung, ymin=0,
                            ymax=(int(preis_solarpanel[0]) / (int(max_earnings_per_years) * 10)), color='black',
                            linestyle='dashed', linewidth=0.5)
                plt.ylabel("Money [€]", fontsize=5)
                plt.xlabel('Time [Years]', fontsize=5)
                plt.text(x=5, y=-20, s="---> Amortsierungpunkt", fontsize=5)
                plt.xticks(np.arange(0, 11, 1),fontsize=5)
                plt.yticks(fontsize=5)
                st.pyplot(plt)


if __name__ == '__main__':
    gui_version_1()
