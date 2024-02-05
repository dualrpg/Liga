import sqlite3 as sql
from utils_csv import read
from pprint import pprint

def createDB():
    conn = sql.connect("liga.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    cursor.execute(
        """DROP TABLE IF EXISTS equipos"""
    )
    cursor.execute(
        """DROP TABLE IF EXISTS jugadores"""
    )
    conn.commit()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS divisiones (
            nombre text
        )        
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS equipos (
            dueño text,
            nombre text,
            division text,
            media int
        )        
        """
    )
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS jugadores (
            nombre text,
            nacionalidad text,
            posicion text,
            media double,
            numero integer,
            equipo text
        )        
        """
    )
    conn.commit()
    conn.close()

def insertRowDivisiones(nombre):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO divisiones VALUES ('{nombre}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def insertRowEquipos(nombre, dueño, division):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO equipos VALUES ('{nombre}', '{dueño}','{division}','')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def insertRowJugadores(nombre, nacionalidad, posicion, media, numero, equipo):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO jugadores VALUES ('{nombre}', '{nacionalidad}', '{posicion}','{media}', '{numero}', '{equipo}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def readInsertEquipos(file):
    equipos = read(file)
    for equipo in equipos:
        nombre = equipo[0].strip()
        dueño = equipo[1].strip()
        division = equipo[2].strip()
        insertRowEquipos(nombre, dueño, division)

def readInsertJugadores(file):
    jugadores = read(file)
    for jugador in jugadores:
        nombre = jugador[0].strip()
        nacionalidad = jugador[1].strip()
        posicion = jugador[2].strip()
        media = jugador[3].strip()
        numero = jugador[4].strip()
        equipo = jugador[5].strip()
        insertRowJugadores(nombre, nacionalidad, posicion, media, numero, equipo)


def media():
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"SELECT equipo, AVG(media) as media_promedio FROM (SELECT equipo, media, ROW_NUMBER() OVER (PARTITION BY equipo ORDER BY media DESC) as ranking FROM jugadores ) AS jugadores_numerados WHERE ranking <= 18 GROUP BY equipo;"
    cursor.execute(instruccion)
    medias = cursor.fetchall()
    for media in medias:
        equipo = media[0]
        media = media[1]
        instruccion = f"UPDATE equipos SET media={media} WHERE nombre LIKE '{equipo}';"
        cursor.execute(instruccion)
        conn.commit()
    conn.close()

    

# createDB()
# createTable()
# readInsertEquipos("EquiposPrimera.csv")
# readInsertJugadores("JugadoresPrimera.csv")
media()