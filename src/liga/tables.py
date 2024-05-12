class statements:
    def __init__(self) -> None:
        pass

    divisiones = [{"division": "Primera"}, {"division": "Segunda"}]
    tablesBase = """DROP TABLE IF EXISTS divisiones;
                    DROP TABLE IF EXISTS equipos;
                    DROP TABLE IF EXISTS jugadores;
                    DROP TABLE IF EXISTS temporada;
                    DROP TABLE IF EXISTS resultados;
                    DROP TABLE IF EXISTS goles;
                    DROP TABLE IF EXISTS lesiones;
                    DROP TABLE IF EXISTS faltas;
                    CREATE TABLE IF NOT EXISTS divisiones (
                        division text
                    );
                    CREATE TABLE IF NOT EXISTS equipos (
                        dueño text,
                        nombre text,
                        division text,
                        media int
                    );
                    CREATE TABLE IF NOT EXISTS jugadores (
                        nombre text,
                        nacionalidad text,
                        posicion1 text,
                        posicion2 text,
                        media double,
                        numero integer,
                        equipo text,
                        amarillas int,
                        rojas int
                    );
                    CREATE TABLE IF NOT EXISTS temporada (
                        id int,
                        jornada text,
                        equipo1 text,
                        equipo2 text,
                        division text
                    );
                    CREATE TABLE IF NOT EXISTS resultados (
                        id int,
                        equipo1 int,
                        equipo2 int
                    );
                    CREATE TABLE IF NOT EXISTS lesiones (
                        id int,
                        jugador text,
                        gravedad text,
                        duracion int
                    );
                    CREATE TABLE IF NOT EXISTS faltas (
                        id int,
                        jugador text,
                        amarillas text,
                        rojas text
                    );
                    CREATE TABLE IF NOT EXISTS intensidad (
                        id int,
                        equipo1 text,
                        equipo2 text
                    );
                    CREATE TABLE IF NOT EXISTS goles(
                        id int,
                        jugador text,
                        minuto int,
                        propia text
                    )
                    """
    selectMedias = """SELECT equipo, AVG(media) as media_promedio FROM (SELECT equipo, media, ROW_NUMBER() OVER (PARTITION BY equipo ORDER BY media DESC) as ranking FROM jugadores ) AS jugadores_numerados WHERE ranking <= 18 GROUP BY equipo;"""

    def equipos(self, tabla):
        table = f"""DROP TABLE IF EXISTS '{tabla}';
                    CREATE TABLE IF NOT EXISTS '{tabla}' (
                        jugador text,
                        posicion text,
                        entrada int,
                        salida int
                    )"""
        return table
