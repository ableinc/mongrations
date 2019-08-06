from pymongo import MongoClient
import motor.motor_asyncio as motor
import pymysql.cursors
import psycopg2
from mongrations.cache import Cache
from os import getcwd, environ
from os.path import basename
import subprocess, shlex, io, sys


# Command Line Interface Class
class MongrationsCli:
    def __init__(self):
        self._cache = Cache()

    @staticmethod
    def _command_line_interface(migrations: list, state: str):
        print(f'{state.upper()}: Running {len(migrations)} migration{"" if len(migrations) <= 1 else "s"}...')
        for migration in migrations:
            command = shlex.split(f'python3 {migration}')
            print(f'=== {basename(migration)} ===')
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, env=environ.copy())
            for line in io.TextIOWrapper(proc.stdout, encoding='utf8', newline=''):
                print(line)

    def down(self):
        environ['MONGRATIONS_MIGRATE_STATE'] = 'DOWN'
        migrations = self._cache.migrations_file_list()
        self._command_line_interface(migrations, 'down')

    def migrate(self):
        environ['MONGRATIONS_MIGRATE_STATE'] = 'UP'
        migrations = self._cache.migrations_file_list()
        self._command_line_interface(migrations, 'migrate')

    def create(self, file_path=getcwd(), name='-no-name-migration'):
        self._cache.new_migration(name, file_path)
    
    def undo(self):
        environ['MONGRATIONS_MIGRATE_STATE'] = 'DOWN'
        migration = self._cache.undo_migration()
        self._command_line_interface([migration], 'undo')


# For Mongration Files
class Connect:
    def __init__(self, connection_object, db_service):
        self._connection_object = connection_object if not None else {}
        self._db_service = db_service
        self._service_selection = None
        self._connection()

    def _connection(self):
        connections = {
            'mongo': {
                'host': self._connection_object.get('MONGO_HOST', None) if not None else environ.get('MONGO_HOST',
                                                                                                     None),
                'port': self._connection_object.get('MONGO_PORT', None) if not None else environ.get('MONGO_PORT',
                                                                                                     27017),
                'db': self._connection_object.get('MONGO_DB', None) if not None else environ.get('MONGO_DB', None)
            },
            'mysql': {
                'host': self._connection_object.get('MYSQL_HOST', None) if not None else environ.get('MYSQL_HOST',
                                                                                                     None),
                'user': self._connection_object.get('MYSQL_USER', None) if not None else environ.get('MYSQL_USER',
                                                                                                     None),
                'password': self._connection_object.get('MYSQL_PASSWORD', None) if not None else environ.get(
                    'MYSQL_PASSWORD', None),
                'port': self._connection_object.get('MYSQL_PORT', None) if not None else environ.get('MYSQL_PORT',
                                                                                                     3306),
                'db': self._connection_object.get('MYSQL_DB', None) if not None else environ.get('MYSQL_DB', None)
            },
            'postgres': {
                'host': self._connection_object.get('POSTGRES_HOST', None) if not None else environ.get('POSTGRES_HOST',
                                                                                                        None),
                'user': self._connection_object.get('POSTGRES_USER', None) if not None else environ.get('POSTGRES_USER',
                                                                                                        None),
                'password': self._connection_object.get('POSTGRES_PASSWORD', None) if not None else environ.get(
                    'POSTGRES_PASSWORD', None),
                'port': self._connection_object.get('POSTGRES_PORT', None) if not None else environ.get('POSTGRES_PORT',
                                                                                                        5432),
                'db': self._connection_object.get('POSTGRES_DB', None) if not None else environ.get('POSTGRES_DB',
                                                                                                    None)
            }
        }
        try:
            for server, configs in connections.items():
                if server == self._db_service:
                    for value in connections[server].values():
                        if value is None:
                            raise KeyError
                    self._service_selection = connections[server]
                    environ['MONGRATIONS_CLASS_TYPE'] = server
            if self._service_selection is None:
                raise KeyError
        except KeyError:
            print('All database configurations required.')
            sys.exit(1)

    def mongo_async(self):
        mongo_url = f'mongodb://{self._service_selection["host"]}:{self._service_selection["port"]}'
        client = motor.AsyncIOMotorClient(mongo_url)
        return client[self._service_selection["db"]]

    def mongo_sync(self):
        mongo_url = f'mongodb://{self._service_selection["host"]}:{self._service_selection["port"]}'
        client = MongoClient(mongo_url)
        return client[self._service_selection["db"]]

    def mysql(self):
        config = self._service_selection
        connection = pymysql.connect(host=config['host'],
                                     user=config['user'],
                                     password=config['password'],
                                     db=config['db'],
                                     port=config['port'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def postgres(self):
        config = self._service_selection
        conn = psycopg2.connect(host=config['host'], database=config['db'], user=config['user'], password=config['password'])
        return conn.cursor()


class Mongrations:
    def __init__(self, migration_class, state: str = 'sync', db_service: str = 'mongo', connection_obj: dict = None):
        self._migration_class = migration_class()
        self.connect = Connect(connection_obj, db_service)
        self.db = None
        self.state = state
        self.connection(db_service)
        if environ['MONGRATIONS_MIGRATE_STATE'] == 'UP':
            self.up()
        elif environ['MONGRATIONS_MIGRATE_STATE'] == 'DOWN':
            self.down()

    def connection(self, db_service):
        db_option = {
            'mongo': {
                'sync': self.connect.mongo_sync,
                'async': self.connect.mongo_async
            },
            'mysql': self.connect.mysql,
            'postgres': self.connect.postgres
        }.get(db_service)
        if isinstance(db_option, dict):
            self.db = db_option[self.state]()
        else:
            self.db = db_option()

    def up(self):
        self._migration_class.up(self.db)

    def down(self):
        self._migration_class.down(self.db)




