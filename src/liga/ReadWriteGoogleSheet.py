from google.oauth2.service_account import Credentials  # type: ignore
import gspread  # type: ignore
from utils import clearName


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)

gc = gspread.service_account(filename="credentials.json")


class archivos:
    googleFile = "Jugadores new ina league"
    sheetJugadores = "BD_Jugadores(No tocar)"
    sheetEquipos = "BD_Equipos(No tocar)"


def read(hoja):
    file = gspread.authorize(creds)
    workbook = file.open(archivos.googleFile)
    sheet = workbook.worksheet(hoja)
    collection = sheet.get_all_values()
    return collection


def indexJugadores():
    collection = read(archivos.sheetJugadores)
    jugadoresIndexed = []
    indexed = {}
    for jugador in collection:
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
        indexed["amarillas"] = ""
        indexed["rojas"] = ""
        jugadoresIndexed.append(indexed.copy())
    return jugadoresIndexed


def indexEquipos():
    collection = read(archivos.sheetEquipos)
    equiposIndexed = []
    indexed = {}
    for equipo in collection:
        indexed["dueño"] = clearName(equipo[0])
        indexed["nombre"] = clearName(equipo[1])
        indexed["division"] = clearName(equipo[2])
        indexed["media"] = ""
        equiposIndexed.append(indexed.copy())
    return equiposIndexed
