import psycopg2
import logging
import contextlib

LOG = logging.getLogger()

def connect(dsn):
    """
        Open a connection to the database.

        The returned object may be used in conjunction with 'with'.
        When used outside a context manager, use the `connection` attribute
        to get the connection.
    """
    try:
        conn = psycopg2.connect(dsn)
        ctxmgr = contextlib.closing(conn)
        ctxmgr.connection = conn
        return ctxmgr
    except psycopg2.OperationalError as err:
        raise Exception("Cannot connect to database: {}".format(err)) from err