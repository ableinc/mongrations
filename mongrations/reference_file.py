from mongrations import Mongrations


class Mongration:
    def __init__(self):
        pass

    @staticmethod
    def up(db):
        pass

    @staticmethod
    def down(db):
        pass


Mongrations(Mongration, 'sync')
