import sqlite3 as sql
from ReadWriteGoogleSheet import readEquipos, readJugadores
from partidos import matchup, schedule, faltas
from utils import readCSV, clearName

divisiones = ["Primera", "Segunda"]

def createDB():
    conn = sql.connect("liga.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    cursor.execute(
        """DROP TABLE IF EXISTS divisiones"""
    )
    cursor.execute(
        """DROP TABLE IF EXISTS equipos"""
    )
    cursor.execute(
        """DROP TABLE IF EXISTS jugadores"""
    )
    conn.commit()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS divisiones (
            division text
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
            posicion1 text,
            posicion2 text,
            media double,
            numero integer,
            equipo text,
            amarillas int,
            rojas int
        )        
        """
    )
    conn.commit()
    conn.close()

def insertRowDivisiones(divisiones):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    for division in divisiones:
        instruccion = f"INSERT INTO divisiones VALUES ('{division}')"
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


def insertRowJugadores(nombre, nacionalidad, posicion1, posicion2, media, numero, equipo):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO jugadores VALUES ('{nombre}', '{nacionalidad}', '{posicion1}', '{posicion2}','{media}', '{numero}', '{equipo}', 0, 0)"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def readInsertEquipos():
    equipos = readEquipos()
    for equipo in equipos:
        dueño = clearName(equipo[0])
        nombre = clearName(equipo[1])
        division = clearName(equipo[2])
        insertRowEquipos(dueño, nombre, division)

def readInsertJugadores():
    jugadores = readJugadores()
    for jugador in jugadores:
        nombre = clearName(jugador[0])
        # nacionalidad = clearName(jugador[1])
        nacionalidad = ""
        # posicion = clearName(jugador[2])
        posicion1 = ""
        posicion2 = ""
        media = jugador[1]
        # numero = clearName(jugador[4])
        numero = ""
        equipo = clearName(jugador[2])
        insertRowJugadores(nombre, nacionalidad, posicion1, posicion2, media, numero, equipo)


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

def listTeamDivision():
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"SELECT division FROM divisiones"
    cursor.execute(instruccion)
    divisiones = cursor.fetchall()
    for division in divisiones:
        temporadaDivision = "temporada" + division[0]
        cursor.execute(
            f"""DROP TABLE IF EXISTS {temporadaDivision}"""
        )
        conn.commit()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {temporadaDivision} (
                id int,
                jornada text,
                equipo1 text,
                equipo2 text,
                resultadoEquipo1 int,
                resultadoEquipo2 int,
                intesidadEquipo1,
                intensidadEquipo2
            )  """
        )
        conn.commit()
        instruccion = f"SELECT nombre FROM equipos WHERE division='{division[0]}';"
        cursor.execute(instruccion)
        equipos = cursor.fetchall()
        teamList = []
        for equipo in equipos:
            teamList.append(equipo[0])
        scheduleList = schedule(teamList)
        gameID = 0
        jornada = 1
        gamesDay = 1
        times = 0
        while times != 2:
            for teamsGame in scheduleList:
                instruccion = f"INSERT INTO {temporadaDivision} VALUES ('{gameID}','{jornada}','{teamsGame[0]}','{teamsGame[1]}','','','','')"
                cursor.execute(instruccion)
                conn.commit()
                gameID += 1
                gamesDay += 1
                if gamesDay == 11:
                    gamesDay = 1
                    jornada += 1
            times += 1
    conn.close()


def teamsDay(jornada):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"SELECT division FROM divisiones"
    cursor.execute(instruccion)
    divisiones = cursor.fetchall()
    for division in divisiones:
        temporadaDivision = "temporada" + division[0]
        instruccion = f"SELECT equipo1, equipo2 FROM {temporadaDivision} WHERE jornada='{jornada}';"
        cursor.execute(instruccion)
        games = cursor.fetchall()
        teamMatch = []
        for game in games:
            for team in game:
                instruccion = f"SELECT nombre, media FROM equipos WHERE nombre='{team}'"
                cursor.execute(instruccion)
                teamAverage = cursor.fetchall()
                teamMatch.append(teamAverage[0])
            results = matchup(teamMatch)
            instruccion = f"UPDATE {temporadaDivision} SET resultadoEquipo1={results[teamMatch[0][0]]} WHERE equipo1='{teamMatch[0][0]}' AND jornada={jornada};"
            cursor.execute(instruccion)
            instruccion = f"UPDATE {temporadaDivision} SET resultadoEquipo2={results[teamMatch[1][0]]} WHERE equipo2='{teamMatch[1][0]}' AND jornada={jornada};"
            cursor.execute(instruccion)
            teamMatch.clear()
    conn.commit()
    conn.close()

def posiciones(file):
    jugadores = readCSV(file)
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    for jugador in jugadores:
        posiciones = jugador[0]
        nombre = clearName(jugador[1])
        i = 1
        for posicion in posiciones.split('/'):
            colum = f"posicion{i}"
            instruccion = f"UPDATE jugadores SET {colum}='{posicion}' WHERE nombre='{nombre}';"
            i += 1
            cursor.execute(instruccion)
    conn.commit()
    conn.close()

def listarJugadoresEquipo(equipo:str):
    conn = sql.connect("liga.db")
    cursor = conn.cursor()
    instruccion = f"SELECT nombre FROM jugadores WHERE equipo='{equipo}'"
    cursor.execute(instruccion)
    listaJugadores = cursor.fetchall()
    conn.close()
    return listaJugadores


if __name__ == "__main__":
    # createDB()
    createTable()
    insertRowDivisiones(divisiones)
    readInsertEquipos()
    readInsertJugadores()
    media()
    listTeamDivision()
    teamsDay(1)
    posiciones("posicionesPrimera.csv")
    posiciones("posicionesSegunda.csv")