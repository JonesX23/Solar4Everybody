"""
This is a sample script to laod shape files and to debug in them.

Test data comes from: https://opendata.stadt-muenster.de/dataset/solarkataster-m%C3%BCnster-solarpotenzial

Information about markdown: https://www.markdownguide.org/cheat-sheet/
"""
import matplotlib.pyplot as plt
import shapefile

def loadShapeFileWithPyShp(filename):
    """
    Function to load the given shape file. Need for this is the python package PyShp: pip install pyshp

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

#das hier habe ich selber mit Tobis Hilfe geschrieben :) yeeeey
#FUNKTION DACHTYPEN
def whichrooftype(shape_input):
    print("Ich bin in die Funktion whichrooftype reingegangen")
    set_rooftypes = set ()
    list_rooftypes = []
    list_rooftypes_count = 0
    Unbekannt = 0
    Spitzdach = 0
    Flachdach = 0

    for record in shape_input.shapeRecords():
        #print(record.record.RoofType)
        set_rooftypes.add (record.record.RoofType)
        list_rooftypes.append (record.record.RoofType)
    print (set_rooftypes)
    print (list_rooftypes)
    list_rooftypes_count = len(list_rooftypes)     #wie viele Elemente sind in der Liste? das wären meine 100%
    for item in list_rooftypes:
        if item == 'Flachdach':
            Flachdach += 1
        elif item == 'Spitzdach':
            Spitzdach += 1
        else:
            Unbekannt += 1
    print(list_rooftypes_count)
    print("Wir haben Flachdächer: " + str(Flachdach))
    print("Wir haben Spitzdächer: " + str(Spitzdach))
    print("Es sind so viele Dächer in unbekannter Form: " +str (Unbekannt))

    #FUNKTION FILTER EFFICIENT ROOFS FOR SOLARENERGY
def effroots (shape_input):
    print ("Ich bin in der Filterfunktion, yeey")

    Gebäudeeignunggut = []
    Gebäudeeignungschlecht =[]
    for record in shape_input.shapeRecords():
        if record.record.Eignung in [1]:                  #wenn ich hier noch eine if sache einfüge, kann ich die Gebäude weiter filtern
            Gebäudeeignunggut.append (record)
        elif record.record.Eignung in [6]:
            Gebäudeeignungschlecht.append(record)
    print ("Wir haben so viele Gebäude, die gut geeignet sind:")
    print (len (Gebäudeeignunggut))
    createPlot(Gebäudeeignunggut)
    plt.show()








def main():
    """
    Main function to
    :return:
    """
    shapeFile2Load = "Solarpotenzial Dachseiten/Solarpotenzial Dachseiten.shp"
    shape_input = loadShapeFileWithPyShp(shapeFile2Load)
    #printTheShapeRecords(shape_input)
    #whichrooftype(shape_input)
    effroots(shape_input)

if __name__ == '__main__':
    main()




