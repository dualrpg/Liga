import sqlite3 as sql
from typing import Any, List


class prueba:
    divisiones = [{"division": "Primera"}, {"division": "Segunda"}]


class control:
    def __init__(self) -> None:
        pass

    def conn(self):
        conn = sql.connect("liga.db")
        cursor = conn.cursor()
        return conn, cursor

    def closeConn(self, conn):
        conn.commit()
        conn.close()

    def execute(self, cursor, instruccion):
        cursor.execute(instruccion)
        return cursor.fetchall()

    def constructorInsert(self, lista, tabla) -> Any:
        instructions = []
        for valores in lista:
            instructions.append(self.generateInsert(tabla, **valores))
        instruccion = self.constructorInstrucciones(instructions)
        return instruccion

    def constructorUpdate(self, lista, tabla, conditionColum, condition) -> Any:
        instructions = []
        for valores in lista:
            instructions.append(
                self.generateUpdate(tabla, conditionColum, condition, **valores)
            )
        instruccion = self.constructorInstrucciones(instructions)
        return instruccion

    def constructorInstrucciones(self, s: list) -> str:
        construido = ""
        if len(s) == 0:
            pass
        else:
            for string in s:
                construido = construido + string + ";"
        return construido

    def generateInsert(self, tabla, **kwargs) -> str:
        valores = ""
        for value in kwargs.values():
            valores = valores + f"'{value}', "
        instruccion = f"INSERT INTO '{tabla}' VALUES ({valores[:-2]})"
        return instruccion

    def generateUpdate(self, tabla, conditionColum, condition, **kwargs) -> str:
        valores = ""
        for key, value in kwargs.items():
            valores = valores + "{0}={1}, ".format(key, value)
        instruccion = f"UPDATE '{tabla}' SET {valores[:-2]} WHERE {conditionColum} LIKE '{condition}"
        return instruccion
