from mongrations import Mongrations, Database
from pydotenvs import load_env, load_env_object

load_env('.env-example')  # by default it looks for .env in the current directory
# connection_object = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


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
        self.remove_column('users', 'isActive')

    def down(self):
        self.drop_table('users')


# To use connection object (parameter): connection_obj = connection_object
Mongrations(Mongration, db_service='postgres')
