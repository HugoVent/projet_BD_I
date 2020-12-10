import sqlite3

""" Create a relation based on a sql table"""

class Database():
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(self.name)

    def get_cursor(self):
        c = self.conn.cursor()
        return c

    def open(self):
        self.conn = sqlite3.connect(self.name)    

    def close(self):
        pass


class Relation():
    def __init__(self, database_cursor, table):
        self.cursor = database_cursor
        self.table = table

    def __str__(self):
        return str(self.table)

    def is_in_database(self):
        pass

    def verify_type(self):
        pass

    def get_column_type(self, column_name):
        pass


class Column():
    def __init__(self, database_cursor, relation):
        pass
