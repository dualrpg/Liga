import partidos
from utils import clearOneValue
import consultas
import getters
import tables


class acciones:
    def __init__(self) -> None:
        self.divisiones = getters.divisiones()
        self.equipos = getters.equipos()
        self.schedule = partidos.schedule()
        self.faltas = partidos.faltas()
        self.lesiones = partidos.lesiones()
        self.goles = partidos.goles()
        self.control = consultas.control()
        self.statements = tables.statements()

    def teamsDay(self, jornada, division):
        conn, cursor = self.control.conn()
        instruccion = f"SELECT equipo1, equipo2, id FROM temporada WHERE jornada='{jornada}' AND division='{division}'"
        cursor.execute(instruccion)
        games = cursor.fetchall()
        teamMatch = []
        matchIDs = []
        for game in games:
            teams = []
            teams.append(game[0])
            teams.append(game[1])
            id_partido = game[2]
            matchIDs.append(id_partido)
            for team in teams:
                instruccion = f"SELECT nombre, media FROM equipos WHERE nombre='{team}'"
                cursor.execute(instruccion)
                teamAverage = cursor.fetchall()
                teamMatch.append(teamAverage[0])
            results = self.goles.matchup(teamMatch, id_partido)
            instruccion = self.control.constructorInsert(results, "resultados")
            cursor.execute(instruccion)
            teamMatch.clear()
        self.control.closeConn(conn)
        return matchIDs

    def insertAsignarFaltas(self, id_partido, intensidad):
        conn, cursor = self.control.conn()
        select = f"SELECT equipo1, equipo2 FROM temporada WHERE id='{id_partido}'"
        equiposPartido = self.control.execute(cursor, select)
        for equipo in equiposPartido[0]:
            jugadores = f"SELECT jugador FROM '{equipo}' WHERE entrada >= 0 AND jugador NOT LIKE 'Propia'"
            lista = self.control.execute(cursor, jugadores)
            cleanList = clearOneValue(lista)
            faltasList = self.faltas.asignarFaltas(id_partido, cleanList, intensidad)
            if not faltasList:
                continue
            instruccion = self.control.constructorInsert(faltasList, "faltas")
            cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def insert_asignar_lesiones(self, id_partido, intensidad):
        conn, cursor = self.control.conn()
        select = f"SELECT equipo1, equipo2 FROM temporada WHERE id='{id_partido}'"
        equiposPartido = self.control.execute(cursor, select)
        for equipo in equiposPartido[0]:
            jugadores = f"SELECT jugador FROM '{equipo}' WHERE entrada >= 0 AND jugador NOT LIKE 'Propia'"
            lista = self.control.execute(cursor, jugadores)
            cleanList = clearOneValue(lista)
            lista_lesiones = self.lesiones.asignarLesiones(
                id_partido, cleanList, intensidad
            )
            instruccion = self.control.constructorInsert(lista_lesiones, "lesiones")
            cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def insert_asignar_goles(self, id_partido):
        conn, cursor = self.control.conn()
        select = f"""SELECT temporada.equipo1  AS equipo1,
                    resultados.equipo1 AS goles1,
                    temporada.equipo2  AS equipo2,
                    resultados.equipo2 AS goles2
                    FROM   temporada
                    JOIN resultados
                    ON temporada.id = resultados.id
                    WHERE  temporada.id = {id_partido}"""
        equiposPartido = self.control.execute(cursor, select)
        equipo1 = equiposPartido[0][:2]
        equipo2 = equiposPartido[0][-2:]
        equiposResultados = [equipo1, equipo2]
        listado_equipos = []
        listado_equipos_ofensivo = []
        for equipo in equiposResultados:
            jugadores = f"SELECT jugador, posicion, entrada, salida FROM '{equipo[0]}' WHERE entrada >= 0"
            lista_jugadores = self.control.execute(cursor, jugadores)
            listado_equipos.append(lista_jugadores)
            jugadores = f"""SELECT jugador, posicion, entrada, salida 
                            FROM '{equipo[0]}' 
                            WHERE entrada >= 0 
                            AND posicion LIKE 'DC'
                            OR posicion LIKE 'MC'"""
            lista_jugadores_ofensivos = self.control.execute(cursor, jugadores)
            listado_equipos_ofensivo.append(lista_jugadores_ofensivos)
        lista_goleadores = self.goles.asignar_goles(
            id_partido, listado_equipos, listado_equipos_ofensivo, equiposResultados
        )
        instruccion = self.control.constructorInsert(lista_goleadores, "goles")
        cursor.executescript(instruccion)
        self.control.closeConn(conn)
