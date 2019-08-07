from mongrations import Mongrations, Database
from pydotenv import load_env, load_env_object

load_env()  # connect via environment variables (default)
# config = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


class Mongration(Database):
    def __init__(self):
        super(Database, self).__init__()

    def up(self):
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            self.db.commit()

            with self.db.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            self.db.close()

    def down(self):
        self.drop_table('users')


Mongrations(Mongration, db_service='mysql')
