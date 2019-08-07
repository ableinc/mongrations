from mongrations import Mongrations, Database
from pydotenv import load_env

load_env()


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        pass

    def down(self):
        pass


Mongrations(Mongration, 'sync')
