from random import choices, shuffle, randint
from collections import Counter
from src.liga.utils import clearName


class goles:
    def __init__(self) -> None:
        pass

    def matchup(self, matchUp, id_partido):
        team1 = matchUp[0]
        team2 = matchUp[1]
        results = choices(
            [team1[0], team2[0], "Fallos"], [team1[1] * 10, team2[1] * 10, 10000], k=15
        )
        counted_results = Counter(results)
        estructura_final = {
            "id": id_partido,
            "equipo1": counted_results[team1[0]],
            "equipo2": counted_results[team2[0]],
        }
        resultado_final = [estructura_final]
        return resultado_final

    def asignar_goles(self, id_partido, listado_gol_random, listado_ofensivos, n_goles):
        j = 0
        jugador = []
        index = {}
        valuesList = []
        asistencia = ""
        while j < 2:
            i = 0
            while i < n_goles[j][1]:
                d20 = randint(1, 20)
                index["id_partido"] = -1
                index["nombre"] = ""
                index["minuto"] = -1
                index["Propia"] = ""
                index["asistencia"] = ""
                if d20 >= 18:
                    choice = choices(listado_gol_random[j], k=1)
                    if choice[0][0] == "Propia":
                        if j == 0:
                            jugador = choices(listado_gol_random[j + 1], k=1)[0]
                            index["Propia"] = "Propia"
                        elif j == 1:
                            jugador = choices(listado_gol_random[j - 1], k=1)[0]
                            index["Propia"] = "Propia"
                    else:
                        jugador = choices(listado_gol_random[j], k=1)[0]
                        asistencia = choices(listado_ofensivos[j], k=1)[0]
                else:
                    jugador = choices(listado_ofensivos[j], k=1)[0]
                    asistencia = choices(listado_ofensivos[j], k=1)[0]
                minuto = randint(jugador[2], jugador[3])
                index["id_partido"] = id_partido
                index["nombre"] = clearName(jugador[0])
                index["minuto"] = minuto
                index["asistencia"] = clearName(asistencia[0])
                valuesList.append(index.copy())
                i += 1
            j += 1
        return valuesList


class schedule:
    def __init__(self) -> None:
        pass

    def createSchedule(self, listado):
        """Create a schedule for the teams in the list and return it"""
        s = []
        shuffle(listado)
        if len(listado) % 2 == 1:
            listado = listado + ["BYE"]

        for i in range(len(listado) - 1):
            mid = int(len(listado) / 2)
            l1 = listado[:mid]
            l2 = listado[mid:]
            l2.reverse()

            # Switch sides after each round
            if i % 2 == 1:
                s = s + [zip(l1, l2)]
            else:
                s = s + [zip(l2, l1)]

            listado.insert(1, listado.pop())

        return s

    def schedule_matches(self, division):
        matches = []
        for round in self.createSchedule(division):
            for match in round:
                matches.append(match)
        return matches


class faltas:
    def __init__(self) -> None:
        pass

    def calcFaltas(self, agresividad: str):
        match agresividad:
            case "blando":
                mod = -5
            case "normal":
                mod = 0
            case "intenso":
                mod = 5
            case _:
                mod = 0
        roll = randint(1, 20)
        result = roll + mod
        nfaltas = result - 14
        if nfaltas < 0:
            nfaltas = 0
        elif nfaltas > 6:
            nfaltas = 6
        return nfaltas

    def asignarFaltas(self, id_partido, listado: list, intensidad):
        nfaltas = self.calcFaltas(intensidad)
        if nfaltas == 0:
            return []
        jugadores = choices(listado, k=nfaltas)
        count = Counter(jugadores)
        check = False
        index = {}
        valuesList = []
        for c in count.items():
            if nfaltas == 6:
                if c[1] >= 2:
                    check = True
            else:
                check = True
            index["id_partido"] = id_partido
            index["nombre"] = clearName(c[0])
            index["amarilla"] = c[1]
            index["roja"] = ""
            valuesList.append(index.copy())
        if check is not True:
            num = randint(0, 5)
            valuesList[num]["amarilla"] = ""
            valuesList[num]["roja"] = 1
        return valuesList


class lesiones:
    def __init__(self) -> None:
        pass

    def calc_lesiones(self, agresividad: str):
        match agresividad:
            case "blando":
                mod = -5
            case "normal":
                mod = 0
            case "intenso":
                mod = 5
            case _:
                mod = 0
        roll = randint(1, 20)
        result = roll + mod
        n_lesiones = result - 17
        if n_lesiones < 0:
            n_lesiones = 0
        elif n_lesiones > 3:
            n_lesiones = 3
        return n_lesiones

    def asignarLesiones(self, id_partido, listado: list, intensidad):
        n_lesiones = self.calc_lesiones(intensidad)
        jugadores = choices(listado, k=n_lesiones)
        count = Counter(jugadores)
        index = {}
        valuesList = []
        for c in count.items():
            d3 = randint(1, 3)
            if d3 == 1:
                gravedad = "Leve"
                maximo_semanas = 2
            elif d3 == 2:
                gravedad = "Media"
                maximo_semanas = 4
            else:
                gravedad = "Grave"
                maximo_semanas = 10
            duracion = randint(1, maximo_semanas)
            index["id_partido"] = id_partido
            index["nombre"] = clearName(c[0])
            index["gravedad"] = gravedad
            index["duración"] = duracion
            valuesList.append(index.copy())
        return valuesList
