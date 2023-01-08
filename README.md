# Mongrations

![alt text](https://img.icons8.com/dusk/64/000000/database.png "Mongrations Logo")
A database independent migration and seeding tool for python. Compatible with MySQL, PostgreSQL and MongoDB.

## Required

  - Python version 3.6 or above
  - pip version 20.3 or above

## Getting Started

1 . Generate a migration file
```bash
mongrations create insert-into-members
```
2 . Contents of the generated migration file (*import and class definition are 
autogenerated for migration file* - **contents of up() and down() are user defined**.)
```python
from mongrations import Mongrations, Database

class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        collection = self.db['members']
        data = {
            'accountId': 1,
            'username': 'admin',
            'email': 'admin@able.digital',
            'firstName': 'Site',
            'lastName': 'Owner'
        }
        collection.insert_one(data)

    def down(self):
        collection = self.db['members']
        collection.delete_one({'username': 'admin'})


Mongrations(Mongration)
```
3 . Run migrations
```bash
mongrations migrate
```

## Install

```bash
pip install --upgrade pip
pip install mongrations
```
or install locally
```bash
git clone https://github.com/ableinc/mongrations.git
cd mongrations
python -m pip install -r requirements.txt
python -m pip install .
```

## Use

Mongrations comes with a CLI Tool and an import class for a pythonic migration approach. PyMongo, PyMySQL & Psycopg2 are used under
the hood, so follow <a href="https://api.mongodb.com/python/current/tutorial.html#getting-a-collection">PyMongo</a>'s,
<a href="https://github.com/PyMySQL/PyMySQL">PyMySQL</a>'s, or <a href="https://github.com/psycopg/psycopg2">Psycopg2</a>'s documentation 
for instructions on how to create your migrations. For the environment variable tool used in this application, follow 
<a href='https://github.com/ableinc/pydotenvs'>this repo</a> (its also installed with this package).

Refer to Mongrations <a href="https://mongrations.readthedocs.io/en/latest/">documentation</a> for more information.

**CLI**
```bash
Usage: mongrations [OPTIONS] COMMAND [ARGS]...

  Mongrations; a database migration tool for Python 3.6 and above.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  create
  down
  inspect
  migrate
  undo
```
**CLI Examples**
```bash
mongrations create [name]  # create new migration (w/ name)
mongrations migrate  # run migrations
mongrations down  # tear down migrations
mongrations undo  # undo last migration
```

**Mongrations Class**
```python
from mongrations import MongrationsCli

migrations = MongrationsCli()

migrations.create(directory='migrations', name='file_name')
migrations.migrate()
migrations.down()
migrations.undo()
```
Run example migration in examples/ folder

## Issues
Please report all issues to repo.

## Notes
You can install psycopg2 from source via setup.py; python setup.py develop. Follow prompts.
You will need root access to development machine to install this tool.

You **MUST** have write access to your file system in order to use this application.

##  Changelog

January 2023:
  - The cache system will now keep the cache file in the ```migrations/``` directory at root
  - psycopg[binary,pool] will now be installed during pip installation (pip 20.3 > is required)
  - Removed the default ```pydotenvs``` import from the migration file
  - Time (in ms) will be appended to file names instead of UUIDs
  - The library wil be getting a rewrite and released under another name. This will be the last major release to the library under this name. Note: bug fixes will still be published.

January 2022:
  - Squashed bugs
  - Mongrations can now run on Linux
  - Default: stdout error output if error occurs during caching operation
  - Removed the psycopg2 install step from setup.py
  - Simplified how the database connection strings are initialized
  - Inspect will now pretty print JSON structure and provide file system location
  - Updated ```examples/``` directory

August 2020:
  - Introduced the official version 1.0.0 of Mongrations!
  - Rewrote command line tool; much easier and intuiative
  - Extracted classes into their own files; reducing clutter
  - Added a raw sql function that allows for much more flexibility
  - File name rewrites (if you encounter an upgrade error run the option: --no-cache, with pip)
  - psycopg2 is now installed optionally (refer to Notes)
  - Super fast writing to the system
  - Setup.py has been cleaned up. An occasional bug occured when installing
  - Added/Updated examples (refer to Github)
