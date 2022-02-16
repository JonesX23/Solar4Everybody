### UserInput 1.Version

##streamlit package installieren
import streamlit as st

##streamlit App designen
def gui_version_1():

 ##1. Schritt: Liegt der Balkon zur Südseite?
    st.write("""  # 1. Schritt
    """)

    kompassgrad = st.number_input('Nutze bitte dein Handy, blablabla')
    if kompassgrad <= 360 and kompassgrad >= 0:

        if kompassgrad <= 225 and kompassgrad >= 125:
            st.write ('Super, dein Balkon liegt auf der Südseite')

##2. Schritt: Platz auf dem Balkon

            st.write("""  # 2. Schritt
            """)
            filter1 = st.number_input('Wie viel freie Fläche hast du auf deinem Balkon für das Balkonkraftwerk zur Verfügung (in cm)?')

        else:
            st.write('Mh, dein Balkon ist nicht so gut geeignet für ein Balkonkraftwerk')
    else:
        st.write ('Oh, bist du dir sicher, dass du die richtige Gradzahl eingegeben hast?')





def main() -> None:
    gui_version_1()

if __name__ =='__main__':
    main()

