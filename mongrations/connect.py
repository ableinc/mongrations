from os import environ
from pymongo import MongoClient
import motor.motor_asyncio as motor
try:
    import pymysql.cursors
    import psycopg2
except ImportError:
    pass


"""
    Updated: August 2020

    This class is used to connect to the specified database. This will handle connections to all
    three supported database servers.

    As the developer you will not need to handle this directly, as it is used within the Database class.
    Refer to documentation for further information.
"""
class Connect:
    def __init__(self):
        self._connection_object = None
        self._db_service = None
        self._service_selection = None
        self.db = None
        self._state = None

    def _connection(self):
        connections = {
            'mongo': {
                'host': environ.get('MONGO_HOST', None) if not None else self._connection_object.get('MONGO_HOST',
                                                                                                     None),
                'port': environ.get('MONGO_PORT', 27017) if not None else self._connection_object.get('MONGO_PORT',
                                                                                                      None),
                'db': environ.get('MONGO_DB', None) if not None else self._connection_object.get('MONGO_DB', None)
            },
            'mysql': {
                'host': environ.get('MYSQL_HOST', None) if not None else self._connection_object.get('MYSQL_HOST',
                                                                                                     None),
                'user': environ.get('MYSQL_USER', None) if not None else self._connection_object.get('MYSQL_USER',
                                                                                                     None),
                'password': environ.get('MYSQL_PASSWORD', None) if not None else self._connection_object.get(
                    'MYSQL_PASSWORD', None),
                'port': environ.get('MYSQL_PORT', 3306) if not None else self._connection_object.get('MYSQL_PORT',
                                                                                                     None),
                'db': environ.get('MYSQL_DB', None) if not None else self._connection_object.get('MYSQL_DB', None)
            },
            'postgres': {
                'host': environ.get('POSTGRES_HOST', None) if not None else self._connection_object.get('POSTGRES_HOST',
                                                                                                        None),
                'user': environ.get('POSTGRES_USER', None) if not None else self._connection_object.get('POSTGRES_USER',
                                                                                                        None),
                'password': environ.get('POSTGRES_PASSWORD', None) if not None else self._connection_object.get(
                    'POSTGRES_PASSWORD', None),
                'port': environ.get('POSTGRES_PORT', 5432) if not None else self._connection_object.get('POSTGRES_PORT',
                                                                                                        None),
                'db': environ.get('POSTGRES_DB', None) if not None else self._connection_object.get('POSTGRES_DB', None)
            }
        }
        try:
            for server, configs in connections.items():
                if server == self._db_service:
                    for value in connections[server].values():
                        if value is None:
                            raise KeyError
                    self._service_selection = connections[server]
            if self._service_selection is None:
                raise KeyError
        except KeyError:
            print('All database configurations required.')
            sys.exit(1)

    def _set(self, connection_object, db_service, state):
        self._connection_object = connection_object if not None else {}
        self._db_service = db_service
        self._state = state
        self._connection()
        self._get_db()

    def _get_db(self):
        db_option = {
            'mongo': {
                'sync': self._mongo_sync,
                'async': self._mongo_async
            },
            'mysql': self._mysql,
            'postgres': self._postgres
        }.get(self._db_service)
        if isinstance(db_option, dict):
            self.db = db_option[self._state]()
        else:
            self.db = db_option()

    def _mongo_async(self):
        mongo_url = f'mongodb://{self._service_selection["host"]}:{self._service_selection["port"]}'
        client = motor.AsyncIOMotorClient(mongo_url)
        return client[self._service_selection["db"]]

    def _mongo_sync(self):
        mongo_url = f'mongodb://{self._service_selection["host"]}:{self._service_selection["port"]}'
        client = MongoClient(mongo_url)
        return client[self._service_selection["db"]]

    def _mysql(self):
        config = self._service_selection
        connection = pymysql.connect(host=config['host'],
                                     user=config['user'],
                                     password=config['password'],
                                     db=config['db'],
                                     port=config['port'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def _postgres(self):
        config = self._service_selection
        conn = psycopg2.connect(host=config['host'], database=config['db'], user=config['user'], password=config['password'])
        return conn

