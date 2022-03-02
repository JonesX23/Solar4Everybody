"""
This is a sample script to laod shape files and to debug in them.

Test data comes from: https://opendata.stadt-muenster.de/dataset/solarkataster-m%C3%BCnster-solarpotenzial

Information about markdown: https://www.markdownguide.org/cheat-sheet/
"""

import matplotlib.pyplot as plt
import shapefile

def loadShapeFileWithPyShp(filename):
    """
    Function to load the given shape file. Need for this is the python package PyShp: pip install pyshp!!!

    Code comes from: https://gis.stackexchange.com/a/113808

    :param filename: The file to load
    :return: shape
    """
    print("Start loading shape files")
    shape = shapefile.Reader(filename)
    return shape

def createPlot(list_of_records):
    for shape in list_of_records:
        print(shape)
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i == len(shape.shape.parts) - 1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i + 1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x, y)

def printTheShapeRecords(shape_input):
    """
    Function to print the records of the shape: Need to plot the python package matplotlib: pip install matplotlib

    Code comes from: https://gis.stackexchange.com/a/286865

    :param shape: shape parameter that holds the records
    :return: None
    """
    createPlot(shape_input.shapeRecords())
    plt.show()



### Datei "Solarpotenzial Dachseiten" öffnen, um
## a) die BuildingID. Bislang kann ich aber nur sagen, wie viele BuildingIDs wir haben.
def bid (shape_input):
    print ("Ich schaue mir gerade die BuildingID's an")

    building = []
    for record in shape_input.shapeRecords():
        if record.record.BuildingID:
            building.append(record)

    print ("Wir haben so viele GebäudeIds insgesamt")
    print (len (building))



## b) die Gesamteignung Photovoltaik darzustellen. Bislang kann ich aber nur sagen, wie viele gut geeignet sind.
def effroots (shape_input):
    print ("Ich schaue mir gerade die Daten der Gesamteignung Photovoltaik an")

    Gebäudeeignungsehrhoch = []
    Gebäudeeignunghoch =[]
    Gebäudeeignungmittel = []
    for record in shape_input.shapeRecords():
        if record.record.Eignung in [1]:                  #wenn ich hier noch eine if sache einfüge, kann ich die Gebäude weiter filtern
            Gebäudeeignungsehrhoch.append(record)
        elif record.record.Eignung in [2]:
            Gebäudeeignunghoch.append(record)
        elif record.record.Eignung in [3]:
            Gebäudeeignungmittel.append(record)

    print ("Wir haben so viele Gebäude, die eine sehr hohe Einstrahlung haben:")
    print (len (Gebäudeeignungsehrhoch))
    print("Wir haben so viele Gebäude, die eine  hohe Einstrahlung haben:")
    print(len(Gebäudeeignunghoch))
    print ("Wir haben so viele Gebäude, die eine mittlere Einstrahlung haben:")
    print (len (Gebäudeeignungmittel))

###c) die Adresse. Hier habe ich Schwierigkeiten ...
def adres (shape_input):
    print ("Ich schaue mir gerade die einzelnen Adressen an")

    Adressenanzahl = []

    for record in shape_input.shapeRecords():
        if record.record.address:
            Adressenanzahl.append (record)

    print ("Wir haben so viele Adressen:")
    print (len (Adressenanzahl))



def main():
    """
    Main function to
    :return:
    """
    shapeFile2Load = "Solarpotenzial Gebäude/Solarpotenzial Gebäude.shp"
    shape_input = loadShapeFileWithPyShp(shapeFile2Load)
    adres(shape_input)

if __name__ == '__main__':
    main()



