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

    """
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.tables = []
        self.cursor = None

    def __str__(self):
        return self.name

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

    def get_cursor(self):
        c = self.conn.cursor()
        return c

class Relation():
    """ Create a relation based on a sql table
    
    Attributes 
    ----------
    database : Database 
        The database that contains the table

    cursor : sqlite3.cursor
    
    table : str
        The name of the table

    arguments_list = list of str
        List of attributes from the table
    """

    def __init__(self, database, table):
        self.database = database
        self.cursor = self.database.get_cursor()
        self.table = table
        self.arguments_list = self.get_attributes()

    def __str__(self):
        return str(self.table)

    def get_attributes(self):
        attributes = {} 
        all_tables = self.cursor.execute('PRAGMA table_info('+self.table+');')
        for tup in all_tables :
            attributes[tup[1]] = tup[2]
            print(tup[1], tup[2])
        return attributes

    def is_in_database(self):
        return self.table in self.database.tables

    def is_in_table(self, column_name):
        return column_name in self.arguments_list

    def verify_type(self, primitive_type, column_name, old_table):
        """ Verify if the type of a constant is equal to the type of a column

        Parameters:
        ----------
        primitive_type: int, str, boolean
            type of the constant
        
        column_name = str
            the name of the column that we are going to check

        old_table = list of str
            to get all the attributes
        """
        arguments_list = old_table.get_attributes()
        if(self.is_in_table(column_name)):
            type_ = arguments_list[column_name]
            if(primitive_type == str):
                if(type_ == ('text') or type_ == ('char')):
                    return True
                else:
                    return False
            elif(primitive_type == int):
                if(type_ ==('int')):
                    return True
                else:
                    return False
            elif(primitive_type == True or primitive_type == False):
                if(type_ ==('bit')):
                    return True
                else:
                    return False
            elif(primitive_type == float):
                if(type_ ==('float')):
                    return True
                else:
                    return False

    def get_column_type(self, column_name):
        """Get the type of a column

        Parameters:
        ----------
        column_name : str
            The name of the column
        """
        all_columns = self.cursor.execute('PRAGMA table_info('+self.table+');')
        all_columns_type = {}
        res = ""
        for tup in all_columns :
            all_columns_type[tup[1]] = tup[2]
        if (column_name in all_columns_type):
            res = all_columns_type.get(column_name)
        return res
       
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
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.operator = None 

    def __str__(self):
        return f'{self.left_expr} {self.operator} {self.right_expr}'

class Eq(Operation):
    """
    A class that represents an equality between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """
    
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "="
    
    def __str__(self):
        return super().__str__()

class Gt(Operation):
    """
    A class that represents an greater than between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = ">"
    
    def __str__(self):
        return super().__str__()

class Gte(Operation):
    """
    A class that represents a greater or equal between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """    
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = ">="
    
    def __str__(self):
        return super().__str__()

class St(Operation):
    """
    A class that represents a smaller than between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """    
    
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "<"
    
    def __str__(self):
        return super().__str__()

class Ste(Operation):
    """
    A class that represents a smaller or equal than between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """  
    def __init__(self, left_expr, right_expr):
        super().__init__(left_expr, right_expr)
        self.operator = "<="
    
    def __str__(self):
        return super().__str__()

class Diff(Operation):
    """
    A class that represents a difference between 2 expressions
    
    ...

    Attributes
    ----------
    same as Operation
    """  
    def __init__(self, left_expr, right_expr):
        super().__init__( left_expr, right_expr)
        self.operator = '<>'

    def __str__(self):
        return super().__str__()

class Cst():
    """ A class that represents a constant value
    
    Attributes  
    ----------

    value : str, int, boolean, ...
        the value of the constant
    """
    def __init__(self, value):
        self.value = value 

    def get_type(self):
        return type(self.value)

    def __str__(self):
        return f'{self.value}'

