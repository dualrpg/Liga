from src.liga.ReadWriteGoogleSheet import indexJugadores, indexEquipos
import src.liga.partidos as partidos
from src.liga.utils import readCSV, clearName
import src.liga.consultas as consultas
import src.liga.getters as getters
import src.liga.tables as tables


class Base:
    def __init__(self) -> None:
        self.divisiones = getters.divisiones()
        self.equipos = getters.equipos()
        self.schedule = partidos.schedule()
        self.faltas = partidos.faltas()
        self.lesiones = partidos.lesiones()
        self.goles = partidos.goles()
        self.control = consultas.control()
        self.statements = tables.statements()
        self.createDB()
        self.createTables()
        self.insertRowDivisiones()
        self.insertJugadores()
        self.posiciones("src/liga/posicionesPrimera.csv")
        self.posiciones("src/liga/posicionesSegunda.csv")
        self.insertEquipos()
        self.createTablesEquipos()
        self.insertTablesEquipos()
        self.media()
        self.listTeamDivision()

    def createDB(self):
        conn, _ = self.control.conn()
        self.control.closeConn(conn)

    def createTables(self):
        conn, cursor = self.control.conn()
        cursor.executescript(self.statements.tablesBase)
        self.control.closeConn(conn)

    def insertRowDivisiones(self):
        conn, cursor = self.control.conn()
        instruccion = self.control.constructorInsert(
            self.statements.divisiones, "divisiones"
        )
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def insertEquipos(self):
        conn, cursor = self.control.conn()
        equipos = indexEquipos()
        instruccion = self.control.constructorInsert(equipos, "equipos")
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def createTablesEquipos(self):
        equiposList = self.equipos.get_nombre()
        conn, cursor = self.control.conn()
        tableList = []
        for equipo in equiposList:
            tabla = self.statements.equipos(equipo[0])
            tableList.append(tabla)
        instruccion = self.control.constructorInstrucciones(tableList)
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def insertTablesEquipos(self):
        equiposList = self.equipos.get_nombre()
        conn, cursor = self.control.conn()
        valuesList = []
        instruccionEquipo = []
        propia = [{"jugador": "Propia", "posicion": "N", "entrada": 0, "salida": 0}]
        for equipo in equiposList:
            insert_propia = self.control.constructorInsert(propia, equipo[0])
            self.control.execute(cursor, insert_propia)
            select = (
                f"SELECT nombre, posicion1 FROM jugadores WHERE equipo='{equipo[0]}'"
            )
            listaJugadores = self.control.execute(cursor, select)
            for jugador, posicion in listaJugadores:
                values = {
                    "jugador": clearName(jugador),
                    "posicion": posicion,
                    "entrada": 0,
                    "salida": 0,
                }
                valuesList.append(values.copy())
            instruccionEquipo.append(
                self.control.constructorInsert(valuesList, equipo[0])
            )
            valuesList.clear()
        instruccion = self.control.constructorInstrucciones(instruccionEquipo)
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def insertJugadores(self):
        conn, cursor = self.control.conn()
        jugadores = indexJugadores()
        instruccion = self.control.constructorInsert(jugadores, "jugadores")
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def media(self):
        conn, cursor = self.control.conn()
        selMedias = self.statements.selectMedias
        medias = self.control.execute(cursor, selMedias)
        instructionList = []
        for media in medias:
            equipo = media[0]
            media = media[1]
            baseStatement = f"UPDATE equipos SET media={media} WHERE nombre='{equipo}'"
            instructionList.append(baseStatement)
        instruccion = self.control.constructorInstrucciones(instructionList)
        cursor.executescript(instruccion)
        self.control.closeConn(conn)

    def listTeamDivision(self):
        divisionesList = self.divisiones.get_division()
        conn, cursor = self.control.conn()
        gameID = 0
        valuesList = []
        instruccionList = []
        for division in divisionesList:
            jornada = 1
            gamesDay = 1
            times = 0
            instruccion = f"SELECT nombre FROM equipos WHERE division='{division[0]}'"
            equipos = self.control.execute(cursor, instruccion)
            teamList = []
            for equipo in equipos:
                teamList.append(equipo[0])
            scheduleList = self.schedule.schedule_matches(teamList)
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
                    instruccion = self.control.generateInsert("temporada", **values)
                    instruccionList.append(instruccion)
                    gameID += 1
                    gamesDay += 1
                    if gamesDay == 11:
                        gamesDay = 1
                        jornada += 1
                times += 1
        instruccionScript = self.control.constructorInstrucciones(instruccionList)
        cursor.executescript(instruccionScript)
        self.control.closeConn(conn)

    def posiciones(self, file):
        jugadores = readCSV(file)
        conn, cursor = self.control.conn()
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
        self.control.closeConn(conn)
