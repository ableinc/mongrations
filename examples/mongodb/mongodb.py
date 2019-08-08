from mongrations import Mongrations, Database
from pydotenv import load_env, load_env_object

load_env('.env-example')  # by default it looks for .env in the current directory
# config = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        self.db['test_collection'].insert_one({'hello': 'world'})

    def down(self):
        self.db['test_collection'].delete_one({'hello': 'world'})


Mongrations(Mongration, 'sync')
