from os import environ
import sys
try:
    from pymongo import MongoClient
    import motor.motor_asyncio as motor
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
        self._connection_object = {}
        self._db_service = None
        self._service_selection = None
        self.db = None
        self._state = None

    def _connection(self):
        connections = {
            'mongodb': {
                'host': environ.get('MONGO_HOST', None) if self._connection_object.get('MONGO_HOST', None) is None else self._connection_object.get('MONGO_HOST', None),
                'port': environ.get('MONGO_PORT', 27017) if self._connection_object.get('MONGO_PORT', 27017) is None else self._connection_object.get('MONGO_PORT', 27017),
                'user': environ.get('MONGO_USER', None) if self._connection_object.get('MONGO_USER', None) is None else self._connection_object.get('MONGO_USER', None),
                'password': environ.get('MONGO_PASSWORD', None) if self._connection_object.get('MONGO_PASSWORD', None) is None else self._connection_object.get('MONGO_PASSWORD', None),
                'db': environ.get('MONGO_DB_NAME', None) if self._connection_object.get('MONGO_DB_NAME', None) is None else self._connection_object.get('MONGO_DB_NAME', None),
                'authSource': environ.get('MONGO_AUTH_SOURCE', 'admin') if self._connection_object.get('MONGO_AUTH_SOURCE', 'admin') is None else self._connection_object.get('MONGO_AUTH_SOURCE', 'admin')
            },
            'mysql': {
                'host': environ.get('MYSQL_HOST', None) if self._connection_object.get('MYSQL_HOST', None) is None else self._connection_object.get('MYSQL_HOST', None),
                'user': environ.get('MYSQL_USER', None) if self._connection_object.get('MYSQL_USER', None) is None else self._connection_object.get('MYSQL_USER', None),
                'password': environ.get('MYSQL_PASSWORD', None) if self._connection_object.get('MYSQL_PASSWORD', None) is None else self._connection_object.get('MYSQL_PASSWORD', None),
                'port': environ.get('MYSQL_PORT', 3306) if self._connection_object.get('MYSQL_PORT', 3306) is None else self._connection_object.get('MYSQL_PORT', 3306),
                'db': environ.get('MYSQL_DB_NAME', None) if self._connection_object.get('MYSQL_DB_NAME', None) is None else self._connection_object.get('MYSQL_DB_NAME', None)
            },
            'postgres': {
                'host': environ.get('POSTGRES_HOST', None) if self._connection_object.get('POSTGRES_HOST', None) is None else self._connection_object.get('POSTGRES_HOST', None),
                'user': environ.get('POSTGRES_USER', None) if self._connection_object.get('POSTGRES_USER', None) is None else self._connection_object.get('POSTGRES_USER', None),
                'password': environ.get('POSTGRES_PASSWORD', None) if self._connection_object.get('POSTGRES_PASSWORD', None) is None else self._connection_object.get('POSTGRES_PASSWORD', None),
                'port': environ.get('POSTGRES_PORT', 5432) if self._connection_object.get('POSTGRES_PORT', 5432) is None else self._connection_object.get('POSTGRES_PORT', 5432),
                'db': environ.get('POSTGRES_DB_NAME', None) if self._connection_object.get('POSTGRES_DB_NAME', None) is None else self._connection_object.get('POSTGRES_DB_NAME', None)
            }
        }
        try:
            conn = connections[self._db_service]
            if None in conn.values() or conn == None:
                raise ValueError
            self._service_selection = conn
        except KeyError:
            print('Error: The database service {} is not supported.'.format(self._db_service))
            sys.exit(95)
        except ValueError:
            print('Error: All database connection strings are required.')
            sys.exit(95)
        return True

    def _set(self, connection_object, db_service, state):
        self._connection_object = connection_object if not None else {}
        self._db_service = db_service
        self._state = state
        self._connection()
        self._get_db()

    def _get_db(self):
        db_option = {
            'mongodb': {
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
        mongo_url = f'mongodb://{self._service_selection["host"]}:{self._service_selection["port"]}/?connectTimeoutMS=15000'
        authSource = self._service_selection.get("authSource", False)
        if authSource and authSource != 'None':
            mongo_url = mongo_url + f'&authSource={authSource}'
        client = motor.AsyncIOMotorClient(mongo_url)
        return client[self._service_selection["db"]]

    def _mongo_sync(self):
        mongo_url = f'mongodb://{self._service_selection["user"]}:{self._service_selection["password"]}@{self._service_selection["host"]}:{self._service_selection["port"]}/?connectTimeoutMS=15000'
        authSource = self._service_selection.get("authSource", False)
        if authSource and authSource != 'None':
            mongo_url = mongo_url + f'&authSource={authSource}'
        client = MongoClient(mongo_url)
        return client[self._service_selection["db"]]

    def _mysql(self):
        config = self._service_selection
        connection = pymysql.connect(host=config['host'],
                                     user=config['user'],
                                     password=config['password'],
                                     db=config['db'],
                                     port=int(config['port']),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def _postgres(self):
        config = self._service_selection
        conn = psycopg2.connect(host=config['host'], database=config['db'], user=config['user'], password=config['password'])
        return conn
