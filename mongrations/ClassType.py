from pymongo.database import Database
from pymysql.cursors import Cursor
from psycopg2.extensions import cursor
from os import environ

db_type = {
    'mongo': Database,
    'mysql': Cursor,
    'postgres': cursor
}.get(environ.get('MONGRATIONS_CLASS_TYPE'), 'mongo')
ClassType = db_type
