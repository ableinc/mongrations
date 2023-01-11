# Various Read, Write & Fetch functions for cached data
import os.path as path
from os import remove, makedirs, getcwd
import json
from datetime import datetime
import time, pkg_resources
from pathlib import Path
import sys


def get_filepath():
    filepath = Path(path.join(getcwd(), "migrations", ".cache.json"))
    if not path.isdir(filepath.parent):
        try:
            makedirs(filepath.parent)
        except FileExistsError:
            pass
    return filepath


class Cache:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        self._file_path = None
        self._reference_file = pkg_resources.resource_filename('mongrations', 'data/template.txt')
        self._mongration_file = pkg_resources.resource_filename('mongrations', 'data/mongrationFile.json')
        self.initial = False
    
    def _set_file_path(self):
        self._file_path = get_filepath()
    
    def _do_inital_write(self):
        if not path.isfile(self._file_path):
            self.initial = True
            self._initial_write()
        else:
            self.initial = False
        self._file_system_check()

    def _get_file_object(self):
        if self._file_path is None:
            raise FileNotFoundError
        with open(self._file_path, 'r', encoding='utf-8') as reader:
            return json.load(reader)

    def _write_file_obj(self, data, migration_name=''):
        new_data = self._collect_meta_data(data, migration_name)
        try:
            with open(self._file_path, 'w', encoding='utf-8') as writer:
                json_obj = json.dumps(new_data, indent=2, sort_keys=True)
                writer.write(json_obj)
        except json.decoder.JSONDecodeError:
            try:
                remove(self._file_path)
            except OSError as error:
                print(f'{self._file_path} could not be saved. Internal error occurred when creating JSON object. Reason: {error}')

    def _collect_meta_data(self, data, migration_name=''):
        new_data = data
        if self.initial:
            new_data.update({'createdAt': str(datetime.now())})

        if migration_name != '':
            old_entries = new_data['migrations']
            old_entries.append(migration_name)
            new_data.update({'migrations': old_entries})

        if len(new_data['migrations']) >= 1:
            new_data.update({'lastMigration': new_data['migrations'][-1]})
        new_data.update({'totalMigrations': len(new_data['migrations'])})
        new_data.update({'updatedAt': str(datetime.now())})
        return new_data

    def _initial_write(self):
        data = {
                  "totalMigrations": 0,
                  "createdAt": "",
                  "updatedAt": "",
                  "lastMigration": "",
                  "migrations": [],
                  "executed": []
                }
        self._write_file_obj(data)

    def _file_system_check(self):
        file_obj = self._get_file_object()
        updated_migrations_list = file_obj['migrations']
        updated_lastMigration = file_obj['lastMigration']
        for mongration in file_obj['migrations']:
            if not path.isfile(mongration):
                updated_migrations_list.remove(mongration)
                if file_obj['lastMigration'] == mongration:
                    updated_lastMigration = ''
        file_obj['migrations'] = updated_migrations_list
        file_obj['lastMigration'] = updated_lastMigration
        self._write_file_obj(file_obj)

    def new_migration(self, name: str, directory: str):
        if '.py' in name:
            name = name.replace('.py', '')
        try:
            d = path.join(getcwd(), directory)
            if not path.isdir(d):
                makedirs(d)
        except FileExistsError:
            print('Warning: Migration name already exists. File will still be created.\n')
        timestamp = str(time.time())[:str(time.time()).index('.')]
        _name_reference = name
        name = name + '_' + timestamp + '.py'
        migration_path = path.join(getcwd(), directory + '/' + name)
        migration_path_relative = path.join(directory + '/' + name)
        if path.isfile(migration_path):
            self.new_migration(_name_reference, directory)
        with open(self._reference_file, 'r', encoding='utf-8') as reference_file:
            with open(migration_path_relative, 'w', encoding='utf-8') as migration_file:
                migration_file.write(reference_file.read())
        self._write_file_obj(self._get_file_object(), migration_path_relative)
        print(f'Created new migration file: {path.basename(migration_path)}')

    def undo_migration(self, remove_migration: bool = False):
        try:
            cache = self._get_file_object()
            if remove_migration:
                cache['migrations'] = cache['migrations'][:-1]
                cache['executed'].remove(cache['migrations'][-1])
                self._write_file_obj(cache)
            return cache['lastMigration']
        except FileNotFoundError:
            print('Cannot undo last migration. No migrations have been created.')
            sys.exit(97)

    def migrations_file_list(self, last_migration=False):
        try:
            cache = self._get_file_object()
            if last_migration:
                return [cache['lastMigration']]
            return cache['migrations']
        except FileNotFoundError:
            print('Cannot do operation. No migrations have been created.')
            sys.exit(97)

    def inspect_cache(self):
        try:
            self._file_system_check()
            cache = self._get_file_object()
            print(json.dumps(cache, indent=2, sort_keys=False))
            print('File location: ', self._file_path)
        except FileNotFoundError:
            print('Cannot inspect. No migrations have been created.')
    
    def create_migration_file(self):
        file_path = path.join(getcwd(), path.basename(self._mongration_file))
        if path.isfile(file_path):
            print('mongrationFile.json already exists at root.')
            sys.exit(94)
        with open(file_path, mode='w', encoding='utf-8') as mf:
            with open(self._mongration_file, mode='r', encoding='utf-8') as open_mf:
                data = json.load(open_mf)
                mf.write(json.dumps(data, indent=2))
    
    def has_executed(self, filepath):
        cache = self._get_file_object()
        if filepath in cache['executed']:
            return True
        return False

