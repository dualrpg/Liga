import csv

name = "Hidetoshi Nakata (7) (C)"


def readCSV(file):
    jugadores = []
    with open(file, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";")
        for row in spamreader:
            jugadores.append(row)
    return jugadores


def clearName(s: str):
    translationTable = str.maketrans("", "", "1234567890()#[]")
    s = s.translate(translationTable).replace("'", "''").strip()
    if s[-2:] == " C":
        return s[:-1].strip()
    else:
        return s


def clearOneValue(lista):
    listado = []
    for value in lista:
        listado.append(value[0])
    return listado
