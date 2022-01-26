from pymysql.connections import Connection
try:
    from pymongo.database import Database
    from psycopg2.extensions import cursor
except ImportError:
    cursor = None
from os import environ

db_type = {
    'mongo': Database,
    'mysql': Connection,
    'postgres': cursor
}.get(environ.get('MONGRATIONS_CLASS_TYPE'))
ClassType = db_type
