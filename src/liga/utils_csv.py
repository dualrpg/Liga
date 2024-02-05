import csv

def read(file):
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        lista = []
        for row in reader:
            lista.append(row)
        return lista