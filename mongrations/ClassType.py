try:
    from pymysql.connections import Connection
    from pymongo.database import Database
    from psycopg2.extensions import cursor
except ImportError:
    cursor = None
    Connection = None
    Database = None
from os import environ

db_type = {
    'mongodb': Database,
    'mysql': Connection,
    'postgres': cursor
}.get(environ.get('MONGRATIONS_CLASS_TYPE'))
ClassType = db_type
