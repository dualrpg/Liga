import sqlite3 as sql

class prueba:
    divisiones = [{"division":"Primera"},{"division":"Segunda"}]

class control:
    def conn():
        conn = sql.connect("liga.db")
        cursor = conn.cursor()
        return conn, cursor

    def closeConn(conn):
        conn.commit()
        conn.close()

    def execute(cursor, instruccion):
        cursor.execute(instruccion)
        return cursor.fetchall()
    
    def constructorInsert(lista, tabla)->str:
        instruccion = []
        for valores in lista:
            instruccion.append(control.generateInsert(tabla, **valores))
        instruccion = control.constructorInstrucciones(instruccion)
        return instruccion
    
    def constructorUpdate(lista, tabla, conditionColum, condition)->str:
        instruccion = []
        for valores in lista:
            instruccion.append(control.generateUpdate(tabla, conditionColum, condition,**valores))
        instruccion = control.constructorInstrucciones(instruccion)
        return instruccion

    def constructorInstrucciones(s):
        construido = ""
        if len(s) == 0:
            pass
        else:
            for string in s:
                construido = construido + string + ";"
        return construido
    
    def generateInsert(tabla, **kwargs):
        valores = ""
        for value in kwargs.values():
            valores = valores + f"'{value}', "
        instruccion = f"INSERT INTO '{tabla}' VALUES ({valores[:-2]})"
        return instruccion

    def generateUpdate(tabla, conditionColum, condition,**kwargs):
        valores = ""
        for key, value in kwargs.items():
            valores = valores + "{0}={1}, ".format(key, value)
        instruccion = f"UPDATE '{tabla}' SET {valores[:-2]} WHERE {conditionColum} LIKE '{condition}"
        return instruccion
    
    

class divisiones:
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT division FROM divisiones"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class equipos:
    def get_nombre():
        conn, cursor = control.conn()
        instruccion = f"SELECT nombre FROM equipos"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_dueño():
        conn, cursor = control.conn()
        instruccion = f"SELECT dueño FROM equipos"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT division FROM equipos"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class jugadores:
    def get_nombre():
        conn, cursor = control.conn()
        instruccion = f"SELECT nombre FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_posicion1():
        conn, cursor = control.conn()
        instruccion = f"SELECT posicion1 FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_posicion2():
        conn, cursor = control.conn()
        instruccion = f"SELECT posicion2 FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo():
        conn, cursor = control.conn()
        instruccion = f"SELECT equipo FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_amarillas():
        conn, cursor = control.conn()
        instruccion = f"SELECT amarillas FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_rojas():
        conn, cursor = control.conn()
        instruccion = f"SELECT rojas FROM jugadores"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class temporada:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_jornada():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo1():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo2():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class resultados:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo1():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo2():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class faltas:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_jugador():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_amarillas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_rojas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class lesiones:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_jugador():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_gravedad():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_duracion():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.execute(cursor, instruccion)
        control.closeConn(conn)
        return consulta
