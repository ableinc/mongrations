# Various Read, Write & Fetch functions for cached data
import os.path as path
from os import remove, makedirs, getcwd
import json
from datetime import datetime
import uuid, pkg_resources
from pathlib import Path


def get_filepath():
    import sys, getpass
    filepath = {
        'darwin': Path(f'/Users/{getpass.getuser()}/.mongrations/cache.json'),
        'windows': Path('C:/Users/Programs Files/.mongrations/cache.json')
    }.get(sys.platform)
    if not path.isdir(filepath.parent):
        try:
            makedirs(filepath.parent)
        except FileExistsError:
            pass
    return filepath


class Cache:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        self._file_path = get_filepath()
        self._reference_file = pkg_resources.resource_filename('mongrations', 'data/template.txt')
        self.initial = None
        if not path.isfile(self._file_path):
            self.initial = True
            self._initial_write()
        else:
            self.initial = False
        self._file_system_check()

    def _get_file_object(self):
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
            except OSError:
                pass
            if self._verbose:
                print(f'{self._file_path} could not be saved. Internal error occurred when creating JSON object.')

    def _collect_meta_data(self, data, migration_name=''):
        new_data = data
        if self.initial:
            new_data.update({'createdAt': str(datetime.now())})

        if migration_name != '':
            old_entries = new_data['migrations']
            old_entries.append(migration_name)
            new_data.update({'migrations': old_entries})

        if len(new_data['migrations']) >= 1:
            new_data.update({'last_migration': new_data['migrations'][-1]})
        new_data.update({'total_migrations': len(new_data['migrations'])})
        new_data.update({'updatedAt': str(datetime.now())})
        return new_data

    def _initial_write(self):
        data = {
                  "total_migrations": 0,
                  "createdAt": "",
                  "updatedAt": "",
                  "last_migration": "",
                  "migrations": []
                }
        self._write_file_obj(data)

    def _file_system_check(self):
        file_obj = self._get_file_object()
        updated_migrations_list = file_obj['migrations']
        updated_last_migration = file_obj['last_migration']
        for mongration in file_obj['migrations']:
            if not path.isfile(mongration):
                updated_migrations_list.remove(mongration)
                if file_obj['last_migration'] == mongration:
                    updated_last_migration = ''
        file_obj['migrations'] = updated_migrations_list
        file_obj['last_migration'] = updated_last_migration
        self._write_file_obj(file_obj)

    def new_migration(self, name: str, directory):
        try:
            makedirs(path.join(getcwd(), directory))
        except FileExistsError:
            pass
        name = str(uuid.uuid4())[:16] + '-' + name + '.py'
        migration_path = path.join(getcwd(), directory + '/' + name)
        reference_file = open(self._reference_file, 'r', encoding='utf-8')
        with open(migration_path, 'w', encoding='utf-8') as migration_file:
            migration_file.write(reference_file.read())
        reference_file.close()
        self._write_file_obj(self._get_file_object(), migration_path)
        print(f'Created new migration: {path.basename(migration_path)}')

    def undo_migration(self, remove_migration: bool = False):
        cache = self._get_file_object()
        if remove_migration:
            cache['migrations'] = cache['migrations'].remove(cache.index(cache['migrations'][-1]))
            self._write_file_obj(cache)
        return cache['last_migration']

    def migrations_file_list(self):
        cache = self._get_file_object()
        return cache['migrations']

    def inspect_cache(self):
        self._file_system_check()
        cache = self._get_file_object()
        print(cache)