from mongrations import Mongrations, Database
from pydotenvs import load_env, load_env_object

load_env('.env-example')  # by default it looks for .env in the current directory
# connection_object = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        raw_sql = "ALTER TABLE users ADD gender NVARCHAR"
        self.raw(raw_sql)

    def down(self):
        self.drop_table('users')


# To use connection object (parameter): connection_obj = connection_object
Mongrations(Mongration, db_service='mysql')  # raw can be used with all three supported DBs (i.e. MySQL, MongoDB & Postgres)
