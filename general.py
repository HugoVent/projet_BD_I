import sqlite3

class Database():
    def __init__(self, name):
        """
        Init a database 
        Args:
            name (str) : The name (or path) of the database
        """
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.tables = []
        self.cursor = None

    def __str__(self):
        return self.name

    def is_in_database(self, table):
        """
        Check if the table is in the database 
        Args:
            table (str) : The name of the table
        """
        return table in self.tables

    def get_all_tables(self):
        """ Get all the tables from the database"""
        return self.tables

    def get_cursor(self):
        c = self.conn.cursor()
        return c

    def open(self):
        """Open and connect to the database"""
        self.conn = sqlite3.connect(self.name)   
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT name from sqlite_master where type= "table"')
        temp_tables = self.cursor.fetchall()
        for table in temp_tables:
            self.tables.append(table[0]) #The index 0 is used because table is a tuple, so we just get the name
 
    def close(self):
        """Save and close the connection to the database"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self = None

   


class Relation():
    """ Create a relation based on a sql table"""

    def __init__(self, database_cursor, table):
        self.cursor = database_cursor
        self.table = table

    def __str__(self):
        return str(self.table)

    def get_attributes(self) :
        #stolen code, to rewrite
        liste = {} 
        infos = self.cursor.execute('PRAGMA table_info('+self.table+');')
        for tup in infos :
            liste[tup[1]] = tup[2]
            print(tup[1], tup[2])
        return liste

    def is_in_database(self, column_name, arguments_list):
        return column_name in arguments_list

    def verify_type(self, primitive_type, column_name, old_table):
        arguments_list = old_table.get_attributes()
        if(self.is_in_database(column_name, arguments_list)):
            print(primitive_type == int)
            input(1)
            type_ = arguments_list[column_name]
            print(column_name)
            input()
            if(primitive_type == str):
                input(2)
                if(type_ == ('text')):
                    return True
                else:
                    return False
            if(primitive_type == int):
                input(3)

                if(type_ ==('int')):
                    return True
                else:
                    return False

    def get_column_type(self, column_name):
        all_columns = self.cursor.execute('PRAGMA table_info('+self.table+');')
        dictio = {}
        for tup in all_columns :
            print(tup[1], tup[2])
            dictio[tup[1]] = tup[2]
        if (column_name in dictio):
            res = dictio.get(column_name)
        print(dictio)
        #return res
       
class Table():

    def __init__(self, database_cursor, name, Expr):
        self.cursor = database_cursor
        self.name = name
        self.table = {}
    
###################################@
