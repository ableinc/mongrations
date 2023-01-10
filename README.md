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
autogenerated* - **contents of up() and down() methods are user defined**.)
```python
from mongrations import Mongrations, Database

# MongoDB example
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
pip install -U mongrations

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

## Multi-instance

If your API uses multiple databases to write and read data, you can provide multiple database connections. This can be achieved by providing a connection object (```connection_obj```) to the ```Mongrations``` class in your migrations file. For a ```connection_obj``` example, please refer to the ```examples/``` folder. You can also do this by prepending the service name to your environment variables.

Supported service names:

  - ```MONGO_```
  - ```MYSQL_```
  - ```POSTGRES_```

Example .env file:

```properties
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB_NAME=myapp
MYSQL_PORT=3306
```

**Note:** ```MONGO_``` service name does **NOT** accept ```MONGO_COLLECTION_NAME```. You will need to provide the collection name in your migration file. The synchronous and asynchronous instances of MongoDB use ```admin``` as the ```authSource``` by default. If you do not want to use ```authSource``` please use ```MONGO_AUTH_SOURCE=None```.

## Issues

Please report all issues to repo.

## Notes

To install psycopg2 source run:

```bash
python install_psycopg2.py
```

You **MUST** have write access to your file system to use this application.

##  Changelog

January 2023 - Version 1.1.1:
  - You can now use the ```mongrationFile.json``` file to add database connection variables. You can refer to an example of this file [here](mongrationFile.json)
    - You can specify the environment with ```--migrationfile``` (default env is development):
    ```bash
    mongrations migrate --file mongrationFile.json --env development
    ```
  - The CLI tool can generate the ```mongrationFile.json``` file for you. Run this command:
    ```bash
    mongrations file
    ```

January 2023 - Version 1.1.0:
  - Fixed bug with CLI tool where directory argument wasn't being passed properly to the migrate function. 
  - The CLI tool has new arguments with better helper descriptions
  - The database connection class has been updated to provide more enhances connection strings
  - The cache system was rebuilt - The way mongrations caches will change in the future
  - ```migrations``` directory will not be created until you create your first migration file
  - Updated error codes and error messages.
  - In the event your PYTHON_PATH is changed and points to a Python version less than 3.6 the CLI tool will prompt you.

January 2023 - Version 1.0.4:
  - The cache system will now keep the cache file in the ```migrations/``` directory at root
  - psycopg[binary,pool] will now be installed during pip installation (pip 20.3 > is required)
  - Removed the default ```pydotenvs``` import from the migration file
  - Time (in ms) will be appended to file names instead of UUIDs
  - The library wil be getting a rewrite and released under another name. This will be the last major release to the library under this name. Note: bug fixes will still be published.

January 2022 - Version 1.0.4:
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
