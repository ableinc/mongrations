from mongrations import Mongrations, ClassType
from pydotenv import load_env

load_env()


class Mongration:
    def __init__(self):
        pass

    @staticmethod
    def up(db: ClassType):
        pass

    @staticmethod
    def down(db: ClassType):
        pass


Mongrations(Mongration, 'sync')
