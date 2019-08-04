from pymongo import MongoClient
import motor.motor_asyncio as motor
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
        environ['MONGOGRATION_MIGRATE_STATE'] = 'DOWN'
        migrations = self._cache.migrations_file_list()
        self._command_line_interface(migrations, 'down')

    def migrate(self):
        environ['MONGOGRATION_MIGRATE_STATE'] = 'UP'
        migrations = self._cache.migrations_file_list()
        self._command_line_interface(migrations, 'migrate')

    def create(self, file_path=getcwd(), name='-no-name-migration'):
        self._cache.new_migration(name, file_path)
    
    def undo(self):
        environ['MONGOGRATION_MIGRATE_STATE'] = 'DOWN'
        migration = self._cache.undo_migration()
        self._command_line_interface([migration], 'undo')


# For Mongration Files
class Connect:
    def __init__(self, connection_object: dict = None):
        self._host = None
        self._port = None
        self._db = None
        self._mongo_url = None
        self._connection_object = connection_object
        self._connection()

    def _connection(self):
        try:
            if self._connection_object is None:
                self._host = environ['MONGO_HOST']
                self._port = environ['MONGO_PORT']
                self._db = environ['MONGO_DB']
            else:
                self._host = self._connection_object.get('MONGO_HOST')
                self._port = self._connection_object.get('MONGO_PORT')
                self._db = self._connection_object.get('MONGO_DB')
        except KeyError:
            print('KeyError: All MongoDB configurations required.')
            sys.exit(1)
        self._mongo_url = f'mongodb://{self._host}:{self._port}'

    def mongrations_async(self):
        client = motor.AsyncIOMotorClient(self._mongo_url)
        return client[self._db]

    def mongrations_sync(self):
        client = MongoClient(self._mongo_url)
        return client[self._db]


class Mongrations:
    def __init__(self, migration_class, state: str = 'sync'):
        self._migration_class = migration_class()
        self.connect = Connect()
        self.db = None
        self.state = state
        self.connection()
        if environ['MONGOGRATION_MIGRATE_STATE'] == 'UP':
            self.up()
        elif environ['MONGOGRATION_MIGRATE_STATE'] == 'DOWN':
            self.down()

    def connection(self):
        if self.state == 'sync':
            self.db = self.connect.mongrations_sync()
        if self.state == 'async':
            self.db = self.connect.mongrations_async()

    def up(self):
        self._migration_class.up(self.db)

    def down(self):
        self._migration_class.down(self.db)




