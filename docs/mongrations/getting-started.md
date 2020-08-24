# Getting Started

Make sure you have both [pip](https://pip.pypa.io/en/stable/installing/) and
at least version of Python 3.6 before starting. Mongrations uses new format
strings introduced in 3.6.

## 1. Install Mongrations
```bash
pip3 install mongrations
```
## 2. Create .env with connection parameters
```bash
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD='password'
MYSQL_PORT=3306
MYSQL_DB='mongrations_test'
```
## 3. Create a migration file
```bash
mongrations create create-members-table
```

## 4. Edit migrations
```python
from mongrations import Mongrations, Database
from pydotenvs import load_env

load_env()  # this will automatically grab your environment variables


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        column_info = {
            'id': 'INT NOT NULL AUTO_INCREMENT',
            'firstName': 'VARCHAR(255) NOT NULL',
            'lastName': 'VARCHAR(255) NOT NULL',
            'username': 'VARCHAR(255) NOT NULL',
            'isActive': 'BOOLEAN'
        }
        self.create_table('users', column_info)
        self.add_column('users', 'email')

    def down(self):
        self.drop_table('users')


Mongrations(Mongration, 'sync', db_service='mysql')
```
## 5. Run migrations
```bash
mongrations migrate
```

