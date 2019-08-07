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
        if len(migrations) == 0:
            print('No migrations to run.')
            sys.exit()
        print(f'{state.upper()}: Running {len(migrations)} migration{"" if len(migrations) <= 1 else "s"}...')
        for migration in migrations:
            command = shlex.split(f'python3 {migration}')
            print(f'=== {basename(migration)} ===')
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, env=environ.copy())
            for line in io.TextIOWrapper(proc.stdout, encoding='utf8', newline=''):
                print(line)
        print('Migrations complete.')

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
        return conn.cursor()


class Database(Connect):
    def __init__(self):
        super(Connect, self).__init__()

    def create_database(self, database_name):
        if self._state == 'mongo':
            raise AttributeError('drop_table() cannot be used with MongoDB')
        if self._state == 'mysql':
            try:
                with self.db.cursor() as cursor:
                    # Create a new record
                    sql = f"CREATE DATABASE `{database_name}`"
                    cursor.execute(sql)

                self.db.commit()
            finally:
                self.db.close()
        else:
            print('Postgres N/A')

    def create_table(self, table_name: str, column_info: dict):
        if self._state == 'mongo': raise AttributeError('create_table() cannot be used with MongoDB')
        if self._state == 'mysql':
            try:
                with self.db.cursor() as cursor:
                    # Create a new record
                    sql = f'CREATE TABLE `{table_name}` ( '
                    for column_name, column_type in column_info.items():
                        sql += f'{column_name} {column_type}, '
                    sql += ')'
                    cursor.execute(sql)
                self.db.commit()
            finally:
                self.db.close()
        else:
            print('Postgres N/A')

    def drop_table(self, table_name: str):
        if self._state == 'mongo':
            raise AttributeError('drop_table() cannot be used with MongoDB')
        if self._state == 'mysql':
            try:
                with self.db.cursor() as cursor:
                    # Create a new record
                    sql = f"DROP TABLE `{table_name}`"
                    cursor.execute(sql)

                self.db.commit()
            finally:
                self.db.close()
        else:
            print('Postgres N/A')

    def add_column(self, table_name: str, column_name: str, data_type: str = 'VARCHAR(255)'):
        if self._state == 'mongo':
            raise AttributeError('add_column() cannot be used with MongoDB')
        if self._state == 'mysql':
            try:
                with self.db.cursor() as cursor:
                    # Create a new record
                    sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {data_type}"
                    cursor.execute(sql)

                self.db.commit()
            finally:
                self.db.close()
        else:
            print('Postgres N/A')

    def remove_column(self, table_name: str, column_name: str):
        if self._state == 'mongo':
            raise AttributeError('remove_column() cannot be used with MongoDB')
        if self._state == 'mysql':
            try:
                with self.db.cursor() as cursor:
                    # Create a new record
                    sql = f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"
                    cursor.execute(sql)

                self.db.commit()
            finally:
                self.db.close()
        else:
            print('Postgres N/A')


class Mongrations:
    def __init__(self, migration_class, state: str = 'sync', db_service: str = 'mongo', connection_obj: dict = None):
        self._migration_class = migration_class()
        self.state = state
        self.connection_object = connection_obj
        self.db_service = db_service
        if environ['MONGRATIONS_MIGRATE_STATE'] == 'UP':
            self._up()
        elif environ['MONGRATIONS_MIGRATE_STATE'] == 'DOWN':
            self._down()

    def _up(self):
        self._migration_class._set(self.connection_object, self.db_service, self.state)
        self._migration_class.up()

    def _down(self):
        self._migration_class._set(self.connection_object, self.db_service, self.state)
        self._migration_class.down()
