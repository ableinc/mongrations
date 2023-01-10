from mongrations.cache import Cache
from os import environ, getcwd, remove
from os.path import basename, join
import subprocess, shlex, io, sys


# Command Line Interface Class
class MongrationsCli:
    def __init__(self):
        self._cache = Cache()
        self._cache._set_file_path()

    @staticmethod
    def _command_line_interface(migrations: list, state: str):
        success = True
        if len(migrations) == 0:
            print('No migrations to run.')
            sys.exit(100)
        print(f'{state.upper()}: Running {len(migrations)} migration{"" if len(migrations) <= 1 else "s"}...')
        for migration in migrations:
            migration_file_path = join(getcwd(), migration)
            command = shlex.split(f'python3 {migration_file_path}')
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, env=environ.copy())
            for line in io.TextIOWrapper(proc.stdout, encoding='utf8', newline=''):
                if line.startswith('Error: '):
                    print(line)
                    success = False
                else:
                    print(f'=== {basename(migration)} ===')
                    print(line)
            if success is False:
                break
        if success:
            print('Migrations complete.')

    def down(self, last_migration_only=False):
        environ['MIGRATION_MIGRATE_STATE'] = 'DOWN'
        migrations = self._cache.migrations_file_list(last_migration=last_migration_only)
        self._command_line_interface(migrations, 'down')

    def migrate(self):
        environ['MIGRATION_MIGRATE_STATE'] = 'UP'
        migrations = self._cache.migrations_file_list()
        self._command_line_interface(migrations, 'migrate')

    def create(self, directory='migrations', name='no_name_migration'):
        self._cache._do_inital_write()
        self._cache.new_migration(name, directory)

    def undo(self):
        environ['MIGRATION_MIGRATE_STATE'] = 'UNDO'
        migration = self._cache.undo_migration()
        self._command_line_interface([migration], 'undo')
        remove(migration)
        self._cache._file_system_check()
    
    def inspector(self):
        self._cache.inspect_cache()
    
    def create_mongration_file(self):
        self._cache.create_migration_file()


class Mongrations:
    def __init__(self, migration_class, state: str = 'sync', db_service: str = 'mongodb', connection_obj: dict = {}):
        self._migration_class = migration_class()
        self.state = state
        self.connection_object = connection_obj
        self.db_service = db_service
        try:
            if environ['MIGRATION_MIGRATE_STATE'] == 'UP':
                self._up()
            elif environ['MIGRATION_MIGRATE_STATE'] == 'DOWN' or environ['MIGRATION_MIGRATE_STATE'] == 'UNDO':
                self._down()
        except KeyError:
            print('Migrations must be run with CLI tool or MongrationsCli class.')
            sys.exit(99)

    def _up(self):
        self._migration_class._set(self.connection_object, self.db_service, self.state)
        self._migration_class.up()

    def _down(self):
        self._migration_class._set(self.connection_object, self.db_service, self.state)
        self._migration_class.down()
