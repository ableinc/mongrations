try:
    from mongrations.connect import Connect
    import sys
    import psycopg2
except ImportError:
    from .connect import Connect

"""
    Updated: August 2020

    This class is a database tool with predefined functions for executing operations on the MySQL or Postgres server.
    This class is not used when writing to MongoDB. If using MongoDB, refer to their PyMongo or Motor documentation.
"""
class Database(Connect):
    def __init__(self):
        super(Connect, self).__init__()

    def _alert(self, func_name, append=''):
        if self._db_service == 'mongo':
            print(f'Error: {func_name}() cannot be used with MongoDB {append if not "" else ""}.')
            sys.exit(101)

    def create_database(self, database_name):
        self._alert(self.create_database.__name__)
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = f"CREATE DATABASE `{database_name}`"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def create_table(self, table_name: str, column_info: dict):
        self._alert(self.create_table.__name__)
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = f'CREATE TABLE `{table_name}` ( '
                for column_name, column_type in column_info.items():
                    sql += f'`{column_name}` {column_type}, '
                updated_sql = sql[:-1]
                updated_sql += ')'
                cursor.execute(updated_sql)
            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def drop_table(self, table_name: str):
        self._alert(self.drop_table.__name__)
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = f"DROP TABLE `{table_name}`"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def add_column(self, table_name: str, column_name: str, data_type: str = 'VARCHAR(255) NOT NULL'):
        self._alert(self.add_column.__name__)
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {data_type}"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def remove_column(self, table_name: str, column_name: str):
        self._alert(self.remove_column.__name__)
        try:
            with self.db.cursor() as cursor:
                # Create a new record
                sql = f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def delete_from(self, table_name, column_name, query):
        self._alert(self.delete_from.__name__, 'or MySQL (Postgres Only)')
        try:
            with self.db.cursor() as cursor:
                # Delete a record
                sql = f"DELETE FROM `{table_name}` WHERE `{column_name}` = {query}"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

    def insert_into(self, table_name, column_info):
        self._alert(self.insert_into.__name__)
        try:
            with self.db.cursor() as cursor:
                sql = f'INSERT INTO `{table_name}` ('
                for column_name in column_info.keys():
                    sql += f'`{column_name}`,'
                s_ql = sql[:-1]
                s_ql += ') VALUES ('
                for value in column_info.values():
                    s_ql += f'`{value}`,'
                updated_sql = s_ql[:-1]
                updated_sql += ')'
                cursor.execute(updated_sql)
            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()
    
    def raw(self, raw_sql):
        try:
            with self.db.cursor() as cursor:
                # Delete a record
                sql = f"{raw_sql}"
                cursor.execute(sql)

            self.db.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ', error)
        finally:
            self.db.close()

