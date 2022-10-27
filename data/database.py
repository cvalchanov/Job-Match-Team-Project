from mariadb import connect
from mariadb.connections import Connection



def _get_connection() -> Connection:
    settings = get_database_settings()
    return connect(
        user = settings[0],
        password = settings[1],
        host = settings[2],
        port = int(settings[3]),
        database = settings[4]
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount


def insert_query_transactional(sql: str, conn: Connection, sql_params=()) -> int:
    cursor = conn.cursor()
    cursor.execute(sql, sql_params)

    return cursor.lastrowid

def get_database_settings():
    with open('data/database.txt', mode='r') as txt_file:
        lines = []
        for line in txt_file:
            lines.append(line.strip('\n'))
    if not lines:
        raise ValueError('File is empty')
    return lines