import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import requests
from streamlit_lottie import st_lottie
import pandas as pd


def gui_version_1():
    st.set_page_config(layout="wide")
    st.title("Solar4Everybody")
    st.subheader(
        "Du interessierst dich dafür, ob sich ein Balkonkraftwerk auf deinem Balkon lohnt? Super, dann bist Du hier genau richtig. Wir leiten dich Schritt für Schritt durch:")

    # 1. Schritt: Liegt der Balkon zur Südseite?
    st.write("""  # 1. Schritt""")
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        # st.image("Kompass.jpeg", width= 150)
        pass
    with col2:
        kompassgrad = st.number_input(
            'In diesem Schritt wollen wir überprüfen, zu welcher Seite (Nord, Ost, Süd oder West) dein Balkon liegt. Nutze hierfür am besten dein Handy und eine geeignete Kompass App. Richte dein Handy so aus, dass du die Himmelsrichtung deines Balkons ablesen kannst.'''
            ' Welche Gradzahl zeigt dein Handy an? Bitte trage diese Zahl in das Feld ein.', min_value=0, max_value=360, value=0)
        if 360 >= kompassgrad >= 0:
            if 225 >= kompassgrad >= 125:
                st.write('Super, dein Balkon liegt auf der Südseite. Geh weiter zu Schritt 2!')
            elif kompassgrad == 0:
                st.write('Gib hier bitte deine Gradzahl an.')
            else:
                st.write('Mh, dein Balkon ist nicht so gut geeignet für ein Balkonkraftwerk')
        else:
            st.write('Oh, bist Du dir sicher, dass Du die richtige Gradzahl eingegeben hast?')

    # 2. Schritt: Platz auf dem Balkon


    if 225 >= kompassgrad >= 125:
        st.write("""  # 2. Schritt""")
        VerfügbarerPLatz = st.selectbox(
            'Wir haben für dich ein Balkonkraftwerk herausgesucht.'
            ' Das Modul hat die folgenden Maße:  1755 x 1038 x 35 mm.'

            ' Hast Du genügend Platz dieses Modul an deinem Balkon anzubringen?',
            ('Ja', 'Nein'), index=1)
        if VerfügbarerPLatz == 'Ja':
            st.write('Wunderbar, dann geh direkt zu Schritt 3!')
        else:
            st.write('Tut uns leid, dann kommt für dich "unser" Balkonkraftwerk nicht in Frage')

        # 3. Schritt: Vorstellung des Panels

        if VerfügbarerPLatz == 'Ja':
            col3, col2 = st.columns([2,1])
            with col3:
                st.write("""  # 3. Schritt""")
                st.write(
                    "Gut, dann wollen wir dir einmal das Balkonkraftwerk vorstellen, welches wir für dich herausgesucht haben."
                    " Dieses Modul gilt als Beispiel für ein Balkonkraftwerk made in Germany."
                    " Disclaimer: Nur ein Beispielmodul #nichtgesponsert")
                URL1 = "https://herr-strom.de/p/balkonkraftwerk-solarfabrik-360-plus-alustaender"
                Produkt1 = "Balkonkraftwerk SolarFabrik 360"
                req1 = requests.get(URL1)
                soup1 = BeautifulSoup(req1.content, "html.parser")
                table1 = soup1.find("meta", attrs={'property': 'og:price:amount'})
                rows1 = table1.prettify()
                preis_solarpanel = re.findall('[0-9]+', rows1)
                st.write(f'Der Preis von {Produkt1} beträgt {preis_solarpanel[0]} €')


            with col3:
                st.write(""
                    'Als nächstes möchten wir dir zeigen, wie lange es dauert bis sich dein Balkonkraftwerk amortisiert hat.'
                    ' Wie sollen wir dies berechnen?'"")

             

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
                    #max_earnings_per_years = watt_integer*current_kwh_price
                    #timepoint_amortisierung = (int(preis_solarpanel[0]))/max_earnings_per_years
                ####

                ###
                ###### STROMPREIS SCRAPE

                preisinput = st.selectbox('Strompreis', ['Wähle die Berechnungsgrundlage', 'aktuellen Marktpreis verwenden', 'eigenen Strompreis verwenden'])
                while preisinput == 'aktuellen Marktpreis verwenden':
                    max_earnings_per_years = watt_integer * current_kwh_price
                    timepoint_amortisierung = (int(preis_solarpanel[0])) / max_earnings_per_years
                ##
                    col3.subheader("Amortisierung")
                    col3.write(f'Die Amortisierung ist berechnet anhand des aktuellen Strompreises {current_kwh_price} € pro kWh. '
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
                    break

            ####################### STROMPREIS INPUT
                while preisinput == 'eigenen Strompreis verwenden':

                    preisinput2 = st.number_input('Wähle deinen Strompreis in Cent pro kWh', 1, 100, key=None)


                    max_earnings_per_years = watt_integer * (preisinput2/100)
                    timepoint_amortisierung = (int(preis_solarpanel[0])) / max_earnings_per_years

                    col3.subheader("Amortisierung")
                    col3.write(f'Die Amortisierung ist berechnet anhand deines aktuellen Strompreises {preisinput2/100} €. pro kWh'
                               f'Hiernach wuerde sich ein Balkonkraftwerk nach {("%.2f" % timepoint_amortisierung)} Jahren amortisieren')
                    berechnungszeitraum_Jahre = 11

                    plt.figure(figsize=(3, 3))
                    plt.plot((np.linspace(int(preis_solarpanel[0]) * -1,
                                          (int(preis_solarpanel[0]) * -1) + (int(max_earnings_per_years) * 10),
                                          berechnungszeitraum_Jahre)), color="blue", linewidth=0.5)
                    plt.axhline(0, xmax=(int(preis_solarpanel[0]) / (int(max_earnings_per_years) * 10)), color='black',
                                linestyle='dashed', linewidth=0.5)
                    plt.axvline(timepoint_amortisierung, ymin=0,
                                ymax=(int(preis_solarpanel[0]) / (int(max_earnings_per_years) * 10)), color='black',
                                linestyle='dashed', linewidth=0.5)
                    plt.ylabel("Money [€]", fontsize=5)
                    plt.xlabel('Time [Years]', fontsize=5)
                    plt.text(x=5, y=-20, s="---> Amortsierungpunkt", fontsize=5)
                    plt.xticks(np.arange(0, 11, 1), fontsize=5)
                    plt.yticks(fontsize=5)
                    st.pyplot(plt)
                    break



                while preisinput != 'Wähle die Berechnungsgrundlage':

                #streamlit

                #Animationen
                    def load_lottieurl(url):
                        r = requests.get(url)
                        if r.status_code !=200:
                            return None
                        return r.json()

                    # Hier wird zunächst der berechnete Verbrauch erfasst
                    # Als Beispielwert wird eine Stromgenerierung von 100 kWh pro Jahr genommen.
                    generierung_total = int(watt_integer)
                    print("Super! Dein Balkonmodul würde jährlich ca.",generierung_total, "kWh erzeugen!")
                    print("Um dir zu veranschaulichen, was Du mit deinem selbst produzierten Strom alles machen kannst, haben wir für dich ein paar Beispiele:")

                    # Um die Vergleiche der Haushaltsgeräte möglichst greifbar zu gestalten, wird die Stromgenerierung (alle in kWh) auf verschiedene Ebenen heruntergebrochen
                    generierung_jahr = generierung_total
                    generierung_monat = generierung_total/12
                    generierung_tag = generierung_total/365
                    generierung_woche = generierung_total/52
                    generierung_stunde = generierung_tag/24

                    #Kühlschrank (108 kWh pro Jahr)
                    nutzung_kuehlschrank = round(generierung_jahr/108*12)
                    print("\n\nDein Kühlschrank könnte mit bei einer jährlichen Generierung von",generierung_total, "kWh insgesamt für ca.",nutzung_kuehlschrank, "Monate laufen!")

                    #Toaster (0,05 kWh für 2 Scheiben)
                    nutzung_toaster = round(generierung_tag/0.05)
                    print("\nTäglich könntest Du mit den", generierung_total, "kWh für Dein Frühstück ca.", nutzung_toaster, "Scheiben Toast toasten!")



                    #Föhn (0,03 kWh für 1 Minuten Nutzung bzw. 1,8 kWh für eine Stunde Nutzung)
                    nutzung_foehn_tag = round(generierung_tag/0.03)
                    nutzung_foehn_woche = round(generierung_woche / 0.03)
                    print("\nMit", generierung_total, "kWh könntest Du Dir täglich für ca.", nutzung_foehn_tag, "Minuten die Haare föhnen. In der Woche wären es ca.", nutzung_foehn_woche, "Minuten")



                    #Router (88 kWh pro Jahr bzw. 0,24 kWh pro Tag)
                    nutzung_router = round( generierung_jahr/0.24)
                    print("\nDein Internet-Router könnte für ca.", nutzung_router, "Tage über Deinen eigenen Solarstrom laufen!")



                    #Waschmaschine (0.8 kWh pro Waschgang)
                    nutzung_waschmaschine = round(generierung_woche/0.8)
                    print("\nWöchentlich könntest Du mit den jährlichen", generierung_total, "kWh ca.", nutzung_waschmaschine,"mal eine handelsübliche Waschmaschine bedienen.")



                    #Handyladung (0,02 kWh pro Handyladung)
                    nutzung_handy = round(generierung_tag/0.02)
                    print("\nDein Smartphone könntest Du mithilfe des Balkonmoduls ca.", nutzung_handy, "mal am Tag laden!")



                    #TV (0,1 kWh pro Stunde)
                    nutzung_tv = round(generierung_tag/0.1)
                    print("\nTäglich könntest du ca.", nutzung_tv,"Stunden mithilfe Deiner Solarenergie fernsehen!")


                    #st.set_page_config(page_title="Haushaltsgeraete", page_icon=":+1:", layout="wide")

                    # ---- HEADER SECTION ----
                    with st.container():
                        st.subheader("Im Folgenden eine Übersicht über Haushaltsgeräte, welche sich (teilweise) mit dem Balkonkraftwerk betreiben ließen!")
                        st.title ("Haushaltsgeräte")
                        st.write("Super! :tada: Dein Balkonmodul würde jährlich",generierung_total, "kWh erzeugen!")

                    # ---- TEXTKÖRPER ----
                    with st.container():
                        st.write("---")
                        #left_column, right_column = st.columns(3)
                        with col3:
                            st.header("Haushaltsgeräte")
                            st.write("##")
                            st.write("Beim Betrachten verschiedener Haushaltsgeräte ergeben sich folgende Möglichkeiten:")
                            st.write("##")
                            st.write("- Dein Kühlschrank könnte beispielsweise mit bei einer jährlichen Generierung von",generierung_total, "kWh insgesamt für ca.",nutzung_kuehlschrank,"Monate laufen!")
                            lottie_fridge = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_VRZFwr.json")
                            st_lottie(lottie_fridge, height=150)
                            st.write("##")
                            st.write("- Täglich könntest Du mit den", generierung_total, "kWh für Dein Frühstück ca.", nutzung_toaster, "Scheiben Toast toasten!")
                            lottie_toaster = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_k8WCTV.json")
                            st_lottie(lottie_toaster, height=150)
                            st.write("##")
                            st.write("- Mit", generierung_total, "kWh könntest Du Dir täglich für ca.", nutzung_foehn_tag, "Minuten die Haare föhnen. In der Woche wären es ca.", nutzung_foehn_woche, "Minuten")
                            st.write("##")
                            st.write("- Dein Internet-Router könnte für ca.", nutzung_router, "Tage über Deinen eigenen Solarstrom laufen!")
                            lottie_router = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_v1mq5ba4.json")
                            st_lottie(lottie_router, height=150)
                            st.write("##")
                            st.write("- Wöchentlich könntest Du mit den jährlichen", generierung_total, "kWh ca.", nutzung_waschmaschine,"mal eine handelsübliche Waschmaschine nutzen.")
                            lottie_waschmaschine = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_3xjhagvt.json")
                            st_lottie(lottie_waschmaschine, height=150)
                            st.write("##")
                            st.write("- Dein Smartphone könntest Du mithilfe des Balkonmoduls ca.", nutzung_handy, "mal am Tag laden!")
                            lottie_smartphone = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ka1ozotw.json")
                            st_lottie(lottie_smartphone, height=150)
                            st.write("##")
                            st.write("- Täglich könntest Du ca.", nutzung_tv,"Stunden mithilfe Deiner Solarenergie fernsehen!")
                            lottie_tv = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_wX69nA.json")
                            st_lottie(lottie_tv, height=150)
                            break
if __name__ == '__main__':
    gui_version_1()
