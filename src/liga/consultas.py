import sqlite3 as sql


class control:
    def conn():
        conn = sql.connect("liga.db")
        cursor = conn.cursor()
        return conn, cursor

    def closeConn(conn):
        conn.commit()
        conn.close()

    def fetch(cursor, instruccion):
        cursor.execute(instruccion)
        return cursor.fetchall()
    
    

class divisiones:
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT division FROM divisiones"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class equipos:
    def get_nombre():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_dueño():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class jugadores:
    def get_nombre():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_posicion1():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_posicion2():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_amarillas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_rojas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class temporada:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_jornada():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo1():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo2():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_division():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class resultados:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo1():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_equipo2():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

class faltas:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_jugador():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_amarillas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
    def get_rojas():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta
    
class lesiones:
    def get_id():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_jugador():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_lesion():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

    def get_duracion():
        conn, cursor = control.conn()
        instruccion = f"SELECT FROM"
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta

def consulta(conn, cursor, instruccion):
        conn, cursor = control.conn()
        consulta = control.fetch(cursor, instruccion)
        control.closeConn(conn)
        return consulta