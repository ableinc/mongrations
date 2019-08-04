from mongrations import Mongrations
from pydotenv import load_env, load_env_object

load_env()  # connect via environment variables (default)
# config = load_env_object()  # connect via dictionary from environment variables [ i.e Connect(config) ]


class Mongration:
    def __init__(self):
        pass

    @staticmethod
    def up(db):
        db['test_collection'].insert_one({'hello': 'world'})

    @staticmethod
    def down(db):
        db['test_collection'].delete_one({'hello': 'world'})


Mongrations(Mongration, 'sync')
