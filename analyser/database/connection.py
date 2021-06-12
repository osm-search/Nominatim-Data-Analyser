import psycopg2
import logging
from psycopg2.extensions import connection

LOG = logging.getLogger()

def connect() -> connection:
    """
        Connect to the nominatim database.
    """
    try:
        conn = psycopg2.connect("dbname=nominatim user=nominatim password=")
        return conn
    except psycopg2.OperationalError as err:
        LOG.fatal('Cannot connect to the database: %s', err)
        raise