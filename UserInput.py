### UserInput (Sarah)

##streamlit package installieren
import streamlit as st

##streamlit App designen
def gui_version_1():

## Willkommenstext
    st.title ("Solar4Everybody")

    st.subheader ("Du interessierst dich dafür, ob sich ein Balkonkraftwerk auf deinem Balkon lohnt? Super, dann bist du hier genau richtig. Wir leiten dich Schritt für Schritt durch:")


 ##1. Schritt: Liegt der Balkon zur Südseite?
    st.write("""  # 1. Schritt
    """)

    col1, col2 = st.columns([1,3])

    with col1:
        st.image("Kompass.jpeg", width= 150)

    with col2:

        kompassgrad = st.number_input('In diesem Schritt wollen wir überprüfen, zu welcher Seite (Nord,Ost,Süd oder West) dein Balkon liegt. Nutze hierfür am besten dein Handy und eine geeignete Kompass App. Richte dein Handy so aus, dass du die Himmelsrichtung vom Balkon ablesen kannst. '
                                      ''
                                      'Welche Gradzahl zeigt dein Handy an? Bitte trage diese Zahl in das Feld ein.', min_value=0, max_value=360)
        if kompassgrad <= 360 and kompassgrad >= 0:

             if kompassgrad <= 225 and kompassgrad >= 125:
                st.write ('Super, dein Balkon liegt auf der Südseite. Geh weiter zu Schritt 2!')

             elif kompassgrad == 0:
                st.write ('Gib hier bitte deine Gradzahl an.')

             else:
                st.write('Mh, dein Balkon ist nicht so gut geeignet für ein Balkonkraftwerk')
        else:
                st.write('Oh, bist du dir sicher, dass du die richtige Gradzahl eingegeben hast?')



##2. Schritt: Platz auf dem Balkon

    if kompassgrad <= 225 and kompassgrad >= 125:
        st.write("""  # 2. Schritt
                            """)
        VerfügbarerPLatz = st.selectbox(
            'Wir haben für dich ein Balkonkraftwerk herausgesucht.'
            '(Disclaimer: Nur ein Beispielmodul #nichtgesponsert)'
            'Das Modul hat die folgenden Maße:  1755 x 1038x 35 mm.'
            
            ' Hast du so viel freien Platz auf dem Balkon?',
            ('Ja', 'Nein'), index= 1)

        if VerfügbarerPLatz == 'Ja':
            st.write('Wunderbar, dann geh direkt zu Schritt 3!')

        else:
            st.write('Tut uns leid, dann kommt für dich "unser" Balkonkraftwerk nicht in Frage')


##3. Schritt: Vorstellung des Panels
        if VerfügbarerPLatz == 'Ja':
            st.write("""  # 3. Schritt
                            """)
            st.write("Gut, dann wollen wir dir einmal das Balkonkraftwerk vorstellen, welches wir für dich herausgesucht haben.")

            ##WEBSCRAPING

            import requests
            from bs4 import BeautifulSoup
            import re

            ## URL aufrufen
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

            st.write(f'Der Preis von {Produkt1} beträgt {Preis1[0]} €')





## Verweis auf die Internetseite,
## Preis
## Hersteller
## Bei einer durchschnittlichen Sonneneinstrahlung, kannst du davon ausgehen, dass sich das Balkonkraftwerk in XY Monaten armotisiert hat.
## Das bedeutet, du kannst XY Toastscheiben toasten














def main() -> None:
    gui_version_1()

if __name__ =='__main__':
    main()

