from consultas import control

ctrl = control()


class generico:
    def __init__(self) -> None:
        pass

    def get_todo_division(self, tabla, division):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT * FROM '{tabla}' WHERE division LIKE '{division}'"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_todo_division_paginacion(self, tabla, division, offset, limit, *args):
        conn, cursor = ctrl.conn()
        string = ""
        for item in args:
            string += item + ","
        string = string[:-1]
        instruccion = f"SELECT {string} FROM '{tabla}' WHERE division LIKE '{division}' LIMIT {offset},{limit}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class goles:
    def __init__(self) -> None:
        pass

    def get_goles_division(self, division, offset, limit):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT * FROM goles INNER JOIN temporada ON temporada.id = goles.id WHERE division = '{division}' LIMIT {offset}, {limit}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class divisiones:
    def __init__(self) -> None:
        pass

    def get_division(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT division FROM divisiones"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class equipos:
    def __init__(self) -> None:
        pass

    def get_all(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT * FROM equipos"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_nombre(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT nombre FROM equipos"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_dueño(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT dueño FROM equipos"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_division(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT division FROM equipos"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_media(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT media FROM equipos"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipos_division(self, division, offset, limit):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT dueño, nombre, media FROM equipos WHERE division = '{division}' LIMIT {offset}, {limit}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class jugadores:
    def __init__(self) -> None:
        pass

    def get_nombre(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT nombre FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_posicion1(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT posicion1 FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_posicion2(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT posicion2 FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipo(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT equipo FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_amarillas(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT amarillas FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_rojas(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT rojas FROM jugadores"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class temporada:
    def __init__(self) -> None:
        pass

    def get_id(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_jornada(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipo1(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipo2(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_division(self, division):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT * FROM temporada WHERE division='{division}'"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_partidos_jornada(self, division, jornada):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT id, equipo1, equipo2 FROM temporada WHERE division LIKE '{division}' AND jornada = {jornada}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class resultados:
    def __init__(self) -> None:
        pass

    def get_id(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipo1(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_equipo2(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_resultados_jornada(self, division, n):
        conn, cursor = ctrl.conn()
        instruccion = f"""SELECT resultados.id, temporada.equipo1, 
        resultados.equipo1, temporada.equipo2, resultados.equipo2 
        FROM resultados INNER JOIN temporada 
        ON temporada.id = resultados.id 
        WHERE temporada.division LIKE '{division}' AND jornada = {n};"""
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class faltas:
    def __init__(self) -> None:
        pass

    def get_id(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_jugador(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_amarillas(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_rojas(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_faltas_division(self, division, offset, limit):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT * FROM faltas INNER JOIN temporada ON temporada.id = faltas.id WHERE division = '{division}' LIMIT {offset}, {limit}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta


class lesiones:
    def __init__(self) -> None:
        pass

    def get_id(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_jugador(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_gravedad(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_duracion(self):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT FROM"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta

    def get_lesiones_division(self, division, offset, limit):
        conn, cursor = ctrl.conn()
        instruccion = f"SELECT lesiones.* FROM lesiones INNER JOIN temporada ON temporada.id = lesiones.id WHERE temporada.division = '{division}' LIMIT {offset}, {limit}"
        consulta = ctrl.execute(cursor, instruccion)
        ctrl.closeConn(conn)
        return consulta
