from pymongo.database import Database
from pymysql.connections import Connection
from psycopg2.extensions import cursor
from os import environ

db_type = {
    'mongo': Database,
    'mysql': Connection,
    'postgres': cursor
}.get(environ.get('MONGRATIONS_CLASS_TYPE'))
ClassType = db_type
