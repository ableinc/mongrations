from mongrations import Mongrations, Database
from pydotenv import load_env, load_env_object

load_env()  # connect via environment variables (default)
# config = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        self.create_table('users')

    def down(self):
        self.drop_table('users')


Mongrations(Mongration, db_service='postgres')
