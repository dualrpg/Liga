from ReadWriteGoogleSheet import indexJugadores, indexEquipos
import partidos
from utils import readCSV, clearName, clearOneValue
import consultas
import getters
import tables

divisiones = getters.divisiones()
equipos = getters.equipos()
schedule = partidos.schedule()
faltas = partidos.faltas()
lesiones = partidos.lesiones()
goles = partidos.goles()
control = consultas.control()
statements = tables.statements()


def createDB():
    conn, _ = control.conn()
    control.closeConn(conn)


def createTables():
    conn, cursor = control.conn()
    cursor.executescript(statements.tablesBase)
    control.closeConn(conn)


def createTablesEquipos():
    equiposList = equipos.get_nombre()
    conn, cursor = control.conn()
    tableList = []
    for equipo in equiposList:
        tabla = statements.equipos(equipo[0])
        tableList.append(tabla)
    instruccion = control.constructorInstrucciones(tableList)
    cursor.executescript(instruccion)
    control.closeConn(conn)


def insertRowDivisiones():
    conn, cursor = control.conn()
    instruccion = control.constructorInsert(statements.divisiones, "divisiones")
    cursor.executescript(instruccion)
    control.closeConn(conn)


def insertEquipos():
    conn, cursor = control.conn()
    equipos = indexEquipos()
    instruccion = control.constructorInsert(equipos, "equipos")
    cursor.executescript(instruccion)
    control.closeConn(conn)


def insertTablesEquipos():
    equiposList = equipos.get_nombre()
    conn, cursor = control.conn()
    valuesList = []
    instruccionEquipo = []
    propia = [{"jugador": "Propia", "posicion": "N", "entrada": 0, "salida": 0}]
    for equipo in equiposList:
        insert_propia = control.constructorInsert(propia, equipo[0])
        control.execute(cursor, insert_propia)
        select = f"SELECT nombre, posicion1 FROM jugadores WHERE equipo='{equipo[0]}'"
        listaJugadores = control.execute(cursor, select)
        for jugador, posicion in listaJugadores:
            values = {
                "jugador": clearName(jugador),
                "posicion": posicion,
                "entrada": 0,
                "salida": 0,
            }
            valuesList.append(values.copy())
        instruccionEquipo.append(control.constructorInsert(valuesList, equipo[0]))
        valuesList.clear()
    instruccion = control.constructorInstrucciones(instruccionEquipo)
    cursor.executescript(instruccion)
    control.closeConn(conn)


def insertJugadores():
    conn, cursor = control.conn()
    jugadores = indexJugadores()
    instruccion = control.constructorInsert(jugadores, "jugadores")
    cursor.executescript(instruccion)
    control.closeConn(conn)


def media():
    conn, cursor = control.conn()
    selMedias = statements.selectMedias
    medias = control.execute(cursor, selMedias)
    instructionList = []
    for media in medias:
        equipo = media[0]
        media = media[1]
        baseStatement = f"UPDATE equipos SET media={media} WHERE nombre='{equipo}'"
        instructionList.append(baseStatement)
    instruccion = control.constructorInstrucciones(instructionList)
    cursor.executescript(instruccion)
    control.closeConn(conn)


def listTeamDivision():
    divisionesList = divisiones.get_division()
    conn, cursor = control.conn()
    gameID = 0
    valuesList = []
    instruccionList = []
    for division in divisionesList:
        jornada = 1
        gamesDay = 1
        times = 0
        instruccion = f"SELECT nombre FROM equipos WHERE division='{division[0]}'"
        equipos = control.execute(cursor, instruccion)
        teamList = []
        for equipo in equipos:
            teamList.append(equipo[0])
        scheduleList = schedule.schedule_matches(teamList)
        while times != 2:
            for teamsGame in scheduleList:
                values = {
                    "id": gameID,
                    "jornada": jornada,
                    "equipo1": teamsGame[0],
                    "equipo2": teamsGame[1],
                    "division": division[0],
                }
                valuesList.append(values.copy())
                instruccion = control.generateInsert("temporada", **values)
                instruccionList.append(instruccion)
                gameID += 1
                gamesDay += 1
                if gamesDay == 11:
                    gamesDay = 1
                    jornada += 1
            times += 1
    instruccionScript = control.constructorInstrucciones(instruccionList)
    cursor.executescript(instruccionScript)
    control.closeConn(conn)


def teamsDay(jornada):
    conn, cursor = control.conn()
    instruccion = f"SELECT division FROM divisiones"
    cursor.execute(instruccion)
    divisiones = cursor.fetchall()
    for division in divisiones:
        instruccion = f"SELECT equipo1, equipo2, id FROM temporada WHERE jornada='{jornada}' AND division='{division[0]}'"
        cursor.execute(instruccion)
        games = cursor.fetchall()
        teamMatch = []
        for game in games:
            teams = []
            teams.append(game[0])
            teams.append(game[1])
            id_partido = game[2]
            for team in teams:
                instruccion = f"SELECT nombre, media FROM equipos WHERE nombre='{team}'"
                cursor.execute(instruccion)
                teamAverage = cursor.fetchall()
                teamMatch.append(teamAverage[0])
            results = goles.matchup(teamMatch, id_partido)
            instruccion = control.constructorInsert(results, "resultados")
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
        for posicion in posiciones.split("/"):
            colum = f"posicion{i}"
            instruccion = (
                f"UPDATE jugadores SET {colum}='{posicion}' WHERE nombre='{nombre}'"
            )
            i += 1
            cursor.execute(instruccion)
    control.closeConn(conn)


def listarJugadoresEquipo(equipo: str):
    conn, cursor = control.conn()
    instruccion = f"SELECT nombre FROM jugadores WHERE equipo='{equipo}'"
    cursor.execute(instruccion)
    listaJugadores = cursor.fetchall()
    conn.close()
    return listaJugadores


def insertAsignarFaltas(id_partido, intensidad):
    conn, cursor = control.conn()
    select = f"SELECT equipo1, equipo2 FROM temporada WHERE id='{id_partido}'"
    equiposPartido = control.execute(cursor, select)
    for equipo in equiposPartido[0]:
        jugadores = f"SELECT jugador FROM '{equipo}' WHERE entrada >= 0"
        lista = control.execute(cursor, jugadores)
        cleanList = clearOneValue(lista)
        faltasList = faltas.asignarFaltas(id_partido, cleanList, intensidad)
        if not faltasList:
            continue
        instruccion = control.constructorInsert(faltasList, "faltas")
        cursor.executescript(instruccion)
    control.closeConn(conn)


def insert_asignar_lesiones(id_partido, intensidad):
    conn, cursor = control.conn()
    select = f"SELECT equipo1, equipo2 FROM temporada WHERE id='{id_partido}'"
    equiposPartido = control.execute(cursor, select)
    for equipo in equiposPartido[0]:
        jugadores = f"SELECT jugador FROM '{equipo}' WHERE entrada >= 0"
        lista = control.execute(cursor, jugadores)
        cleanList = clearOneValue(lista)
        lista_lesiones = lesiones.asignarLesiones(id_partido, cleanList, intensidad)
        instruccion = control.constructorInsert(lista_lesiones, "lesiones")
        cursor.executescript(instruccion)
    control.closeConn(conn)


def insert_asignar_goles(id_partido):
    conn, cursor = control.conn()
    select = f"""SELECT temporada.equipo1  AS equipo1,
                resultados.equipo1 AS goles1,
                temporada.equipo2  AS equipo2,
                resultados.equipo2 AS goles2
                FROM   temporada
                JOIN resultados
                ON temporada.id = resultados.id
                WHERE  temporada.id = {id_partido}"""
    equiposPartido = control.execute(cursor, select)
    equipo1 = equiposPartido[0][:2]
    equipo2 = equiposPartido[0][-2:]
    equiposResultados = [equipo1, equipo2]
    listado_equipos = []
    listado_equipos_ofensivo = []
    for equipo in equiposResultados:
        jugadores = f"SELECT jugador, posicion, entrada, salida FROM '{equipo[0]}' WHERE entrada >= 0"
        lista_jugadores = control.execute(cursor, jugadores)
        listado_equipos.append(lista_jugadores)
        jugadores = f"""SELECT jugador, posicion, entrada, salida 
                        FROM '{equipo[0]}' 
                        WHERE entrada >= 0 
                        AND posicion LIKE 'DC'
                        OR posicion LIKE 'MC'"""
        lista_jugadores_ofensivos = control.execute(cursor, jugadores)
        listado_equipos_ofensivo.append(lista_jugadores_ofensivos)
    lista_goleadores = goles.asignar_goles(
        id_partido, listado_equipos, listado_equipos_ofensivo, equiposResultados
    )
    print(lista_goleadores)
    instruccion = control.constructorInsert(lista_goleadores, "goles")
    cursor.executescript(instruccion)
    control.closeConn(conn)


if __name__ == "__main__":
    createDB()
    createTables()
    insertRowDivisiones()
    insertEquipos()
    insertJugadores()
    media()
    listTeamDivision()
    teamsDay(1)
    posiciones("posicionesPrimera.csv")
    posiciones("posicionesSegunda.csv")
    createTablesEquipos()
    insertTablesEquipos()
    insertAsignarFaltas(0, "normal")
    insert_asignar_lesiones(0, "normal")
    insert_asignar_goles(0)
