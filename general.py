import sqlite3

class Database():
    """ 
    A class that represents a Database
    ...

    Attributes
    ----------
    name : str
        The name (or path) of the database

    conn : sqlite3.Connection
        Connecting to the SQLite database

    table : list of str
        A list that contains all the tables from the database

    cursor : sqlite3.Cursor
        A cursor that can performs SQL commands

    operator : str
        The operator of the operation (=, >=, >, <, <=, <>) 

    Methods
    -------
    is_in_database(table)
        Return True if the table is in the database, else it returns False

    get_all_tables():
        Get all the tables from the database
    
    start():
        Start the connection to the database

    close():
        Save and close the connection to the database

    """
    def __init__(self, name):
        """
        Init a database 
        Args:
            name (str) : 
        """
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.tables = []
        self.cursor = None

    def __str__(self):
        return self.name

    def is_in_database(self, table):
        """ Check if the table is in the database 
        
        Parameters:
        ------
        table : str 
        """
        return table in self.tables

    def get_all_tables(self):
        """ Get all the tables from the database"""
        return self.tables

    def start(self):
        """Start the connection connect to the database"""
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

    def get_cursor(self): #to delete
        c = self.conn.cursor()
        return c

class Operation():
    """ 
    A class that represents an operation between 2 expressions
    
    ...

    Attributes
    ----------
    left_expr : str or Cst
        The left expression in a operation, can be a constant or a column name

    right_expr : str or Cst
        The right expression in a operation, can be a constant or a column name

    operator : str
        The operator of the operation (=, >=, >, <, <=, <>) 

    """

    def __init__(self, left_expr, right_expr):
        """
        Parameters
        ----------
        left_expr : str or Cst
            The left expression in a operation, can be a constant or a column name

        right_expr : str or Cst
            The right expression in a operation, can be a constant or a column name
        
        operator : str
            The operator of the operation (=, >=, >, <, <=, <>) 
        """
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.operator = None 

    def __str__(self):
        return f'{self.left_expr} {self.operator} {self.right_expr}'
####################################################

class Eq(Operation):
    """
    A class that represents an operation between 2 expressions
    
    ...

    Attributes
    ----------
    left_expr : str or Cst
        The left expression in a operation, can be a constant or a column name

    right_expr : str or Cst
        The right expression in a operation, can be a constant or a column name

    operator : str
        The operator of the operation (=, >=, >, <, <=, <>) 
    """
    
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "="
    
    def __str__(self):
        return super().__str__()
class Gt(Operation):
    """Greater than..."""
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = ">"
    
    def __str__(self):
        return super().__str__()

class Gte(Operation):
    """Greater than..."""
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = ">="
    
    def __str__(self):
        return super().__str__()

class St(Operation):
    """Greater than..."""
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "<"
    
    def __str__(self):
        return super().__str__()

class Ste(Operation):
    """Greater than..."""
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "<="
    
    def __str__(self):
        return super().__str__()

class Diff(Operation):
    def __init__(self, left_expr, right_expr):
        super().__init__( left_expr, right_expr)
        self.operator = '<>'

    def __str__(self):
        return super().__str__()




class Cst():
    def __init__(self, value):
        self.value = value 

    def get_type(self):
        return type(self.value)

    def __str__(self):
        return f'"{self.value}"'
####################################################

class Relation():
    """ Create a relation based on a sql table"""

    def __init__(self, database, table):
        self.database = database
        self.cursor = self.database.cursor
        self.table = table

    def __str__(self):
        return str(self.table)

    def get_attributes(self) :
        liste = {} 
        infos = self.cursor.execute('PRAGMA table_info('+self.table+');')
        for tup in infos :
            liste[tup[1]] = tup[2]
            print(tup[1], tup[2])
        return liste

    def is_in_database_(self):
        print(self.database.tables)
        return self.table in self.database.tables

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
       
    
###################################@
