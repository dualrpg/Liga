import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes=scope)

def readJugadores():
    file = gspread.authorize(creds)
    workbook = file.open(archivos.googleFile)
    sheet = workbook.worksheet(archivos.sheetJugadores)
    list = sheet.get_all_values()
    return list

def readEquipos():
    file = gspread.authorize(creds)
    workbook = file.open(archivos.googleFile)
    sheet = workbook.worksheet(archivos.sheetEquipos)
    list = sheet.get_all_values()
    return list

class archivos:
    googleFile = "Jugadores new ina league"
    sheetJugadores = "BD_Jugadores(No tocar)"
    sheetEquipos = "BD_Equipos(No tocar)"
    