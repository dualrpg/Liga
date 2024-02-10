import sqlite3 as sql
from ReadWriteGoogleSheet import indexJugadores, indexEquipos
from partidos import matchup, schedule, faltas
from utils import readCSV, clearName
from consultas import control

class statemets:
    divisiones = [{"division":"Primera"},{"division":"Segunda"}]
    tablesBase = """DROP TABLE IF EXISTS divisiones;
                    DROP TABLE IF EXISTS equipos;
                    DROP TABLE IF EXISTS jugadores;
                    CREATE TABLE IF NOT EXISTS equipos (
                        dueño text,
                        nombre text,
                        division text,
                        media int
                    );
                    CREATE TABLE IF NOT EXISTS jugadores (
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

def createDB():
    conn = sql.connect("liga.db")
    control.closeConn(conn)

def createTables():
    conn, cursor = control.conn()
    control.execute(cursor, statemets.tablesBase)
    control.closeConn(conn)

def insertRowDivisiones():
    conn, cursor = control.conn()
    instruccion = control.constructorRow(statemets.divisiones, "divisiones")
    control.execute(cursor, instruccion)
    control.closeConn(conn)


def insertRowEquipos(nombre, dueño, division):
    conn, cursor = control.conn()
    instruccion = control.constructorRow()
    cursor.execute(instruccion)
    control.closeConn(conn)


def insertRowJugadores(nombre, nacionalidad, posicion1, posicion2, media, numero, equipo):
    conn, cursor = control.conn()
    instruccion = f"INSERT INTO jugadores VALUES ('{nombre}', '{nacionalidad}', '{posicion1}', '{posicion2}','{media}', '{numero}', '{equipo}', 0, 0)"
    cursor.execute(instruccion)
    control.closeConn(conn)

def readInsertEquipos():
    equipos = readEquipos()
    indexed = {}
    for equipo in equipos:
        indexed["dueño"] = clearName(equipo[0])
        indexed["nombre"] = clearName(equipo[1])
        indexed["division"] = clearName(equipo[2])
        insertRowEquipos(indexed)

def readInsertJugadores():
    jugadores = readJugadores()
    indexed = {}
    for jugador in jugadores:
        indexed["nombre"] = clearName(jugador[0])
        # indexed["nacionalidad"] = clearName(jugador[1])
        indexed["nacionalidad"] = ""
        # indexed["posicion"] = clearName(jugador[2])
        indexed["posicion1"] = ""
        indexed["posicion2"] = ""
        indexed["media"] = jugador[1]
        # indexed["numero"] = clearName(jugador[4])
        indexed["numero"] = ""
        indexed["equipo"] = clearName(jugador[2])
        insertRowJugadores(indexed)


def media():
    conn, cursor = control.conn()
    instruccion = f"SELECT equipo, AVG(media) as media_promedio FROM (SELECT equipo, media, ROW_NUMBER() OVER (PARTITION BY equipo ORDER BY media DESC) as ranking FROM jugadores ) AS jugadores_numerados WHERE ranking <= 18 GROUP BY equipo"
    cursor.execute(instruccion)
    medias = cursor.fetchall()
    for media in medias:
        equipo = media[0]
        media = media[1]
        instruccion = f"UPDATE equipos SET media={media} WHERE nombre LIKE '{equipo}'"
        cursor.execute(instruccion)
        control.closeConn(conn)

def listTeamDivision():
    conn, cursor = control.conn()
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
        instruccion = f"SELECT nombre FROM equipos WHERE division='{division[0]}'"
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
    conn, cursor = control.conn()
    instruccion = f"SELECT division FROM divisiones"
    cursor.execute(instruccion)
    divisiones = cursor.fetchall()
    for division in divisiones:
        temporadaDivision = "temporada" + division[0]
        instruccion = f"SELECT equipo1, equipo2 FROM {temporadaDivision} WHERE jornada='{jornada}'"
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
            instruccion = f"UPDATE {temporadaDivision} SET resultadoEquipo1={results[teamMatch[0][0]]} WHERE equipo1='{teamMatch[0][0]}' AND jornada={jornada}"
            cursor.execute(instruccion)
            instruccion = f"UPDATE {temporadaDivision} SET resultadoEquipo2={results[teamMatch[1][0]]} WHERE equipo2='{teamMatch[1][0]}' AND jornada={jornada}"
            cursor.execute(instruccion)
            teamMatch.clear()
    control.closeConn(conn)

def posiciones(file):
    jugadores = readCSV(file)
    conn, cursor = control.conn()
    for jugador in jugadores:
        posiciones = jugador[0]
        nombre = clearName(jugador[1])
        i = 1
        for posicion in posiciones.split('/'):
            colum = f"posicion{i}"
            instruccion = f"UPDATE jugadores SET {colum}='{posicion}' WHERE nombre='{nombre}'"
            i += 1
            cursor.execute(instruccion)
    control.closeConn(conn)

def listarJugadoresEquipo(equipo:str):
    conn, cursor = control.conn()
    instruccion = f"SELECT nombre FROM jugadores WHERE equipo='{equipo}'"
    cursor.execute(instruccion)
    listaJugadores = cursor.fetchall()
    conn.close()
    return listaJugadores


if __name__ == "__main__":
    # createDB()
    # createTables()
    insertRowDivisiones()
    # readInsertEquipos()
    # readInsertJugadores()
    # media()
    # listTeamDivision()
    # teamsDay(1)
    # posiciones("posicionesPrimera.csv")
    # posiciones("posicionesSegunda.csv")