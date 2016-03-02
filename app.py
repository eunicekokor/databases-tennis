from psycopg2 import connect, extras

#
# Setup for DB
#
def dict_cursor(conn, cursor_factory=extras.RealDictCursor):
    return conn.cursor(cursor_factory=cursor_factory)


