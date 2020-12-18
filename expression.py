from general import *
import sqlite3

class Expr():
    """Class that represents an abstract expression in SPJRUD
        
        Attributes:
        ----------
        relation : Relation or Expr
            Relation on which the expression is executed

        is_sub_expr : boolean
            To see if the expression is a sub-expression

        old_table : Relation
        
        Notes
        ----------
        The meaning of 'self.old_table' is explained in the readme
    """

    def __init__(self, relation):
        self.relation = relation
        self.is_sub_expr = False
        if isinstance(relation, Relation):
            self.old_table = relation
        elif isinstance(relation, Expr):
            self.old_table = relation.old_table
        else:
            self.old_table = None

    def to_table(self, new_name, database):
        """ Use a SPJRUD query to create a new table
        Attributes:
        ----------
        new_name : str
            The name of the new table
        
        database : Database 
            The database on which the table will be created
        """
        query = self.compile() 
        cursor = database.cursor
        res = f'CREATE TABLE {new_name} AS {query}'     
        cursor.execute(res)     

    def get_attributes(self):
        attributes = {}
        old_attributes = self.old_table.get_attributes()
        for attribute in self.list_attributes:
                if attribute in old_attributes:
                    attributes[attribute] = old_attributes[attribute]
        return attributes

    def to_SQL(self, database):
        """Execute the SQL query and return the result
        Attributes:
        ----------
        new_name : str
            The name of the new table
        
        database : Database 
            The database on which the request will be executed
        """
        self.verify()
        cursor = database.cursor
        query = self.compile()
        cursor.execute(query)
        return cursor.fetchall()

    def get_attributes(self):
        return self.old_table.get_attributes()

class Select(Expr):
    """ Class that represents the Select in SPJRUD
        
        Attributes:
        ----------
        operator : Operation
            Basic operations between 2 elements (=, >, <, >=, <=)

        relation : Relation or Expr
            Relation on which the select is executed

    """
    def __init__(self, operator, relation):
        super().__init__(relation)
        self.operator = operator
        
    def verify(self):
        """ Checks if the operation is valid """
        if not self.relation.is_in_database():
            raise Exception("the relation is not in the table") 
        else:
            if isinstance(self.relation, Expr): 
                #If the raltion is a SPJRUD expression, it is first compiled
                self.relation.is_sub_expr = True
                self.relation = self.relation.compile()
            if isinstance(self.operator, Operation):
                if isinstance(self.operator.right_expr, Cst):
                    if isinstance(self.operator.left_expr, Cst):
                        raise Exception("Can not compare a constant to constant")
                    else:
                        #On suppose que si une constante n'est pas entrée, c'est forcément le nom d'une colonne
                        if self.old_table.is_in_table(self.operator.left_expr):
                            cst_type = self.operator.right_expr.get_type()
                            if(self.old_table.verify_type(cst_type, self.operator.left_expr, self.old_table)):
                                #Verify if the type of the constant is the same as the one in the relation
                                self.operator.right_expr = f'\'{self.operator.right_expr}\''
                            else:
                                prob = f'Invalid expression. The (sub-)expression {self} is invalid because the type of the constant {self.operator.right_expr} which is {cst_type} is not the same as {self.operator.left_expr} which is {self.relation.get_column_type(self.operator.left_expr)}' 
                                raise Exception(prob)
                        else:
                            raise Exception("The column is not in the relation")
                else:
                    #In that case, the operation is on 2 columns
                    attributes = self.old_table.get_attributes() #
                    if self.operator.left_expr in attributes and self.operator.right_expr in attributes:
                        if not (attributes[self.operator.left_expr] == attributes[self.operator.right_expr]):
                            raise Exception("The attributes have different types")
            else:
                raise Exception((self.operator) + 'is not a valid operation')

    def compile(self):
        """Compile the Select to a SQL query"""
        condition = f'SELECT * FROM {self.relation} WHERE {self.operator}' 
        if(self.is_sub_expr):
            condition = f'({condition})'
        return condition     
              
    def get_attributes(self):
        return self.old_table.get_attributes()

class Proj(Expr):
    """ Class that represents the Project in SPJRUD
        
        Attributes:
        ----------
        list_attributes : list of str 
            List of all the column that will be projected

        relation : Relation or Expr
            Relation on which the project is executed
    """
    
    def __init__(self, list_attributes, relation):
        super().__init__(relation)
        self.list_attributes = list_attributes

    def verify(self):
        """ Checks if the operation is valid """
        if isinstance(self.relation, Relation):
            table_elem = self.relation.get_attributes()
            for attribute in self.list_attributes:
                if attribute not in table_elem:
                    raise Exception(f'The attribute \'{attribute}\' is not in the relation {self.relation}')
        elif isinstance(self.relation, Expr):
            self.relation.is_sub_expr = True
            table_elem = self.relation.old_table.get_attributes()
            self.relation = self.relation.compile() 

            for attribute in self.list_attributes:
                if attribute not in table_elem:
                    raise Exception(f'The attribute \'{attribute}\' is not in the relation {self.relation}')

    def compile(self):
        """Compile the Proj to a SQL query"""
        attributes = ''
        for i in range(len(self.list_attributes)):
            attributes += self.list_attributes[i]
            if i != (len(self.list_attributes) - 1):
                attributes += ", "
        condition = f'SELECT DISTINCT {attributes} FROM ({self.relation})'
        if self.is_sub_expr:
            condition = f'({condition})' 
        return condition

class Join(Expr):
    """ Class that represents the Join in SPJRUD
        
        Attributes:
        ----------
        left_expr : Relation or Expr
            The left expression of the join

        right_expr : Relation or Expr
            The right expression of the join

        relation : Relation or Expr
            Relation on which the join is executed

    """
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.list_attributes_1 = None
        self.list_attributes_2 = None
        self.common_attributes = []

    def verify(self):
        """ Checks if the operation is valid """
        left_attributes = self.left_expr.get_attributes()
        right_attributes = self.right_expr.get_attributes()
        if isinstance(self.left_expr, Expr):
            self.left_expr = self.left_expr.compile()
        elif isinstance(self.left_expr, Relation):
            if not self.left_expr.is_in_database():
                raise Exception(f'{self.left_expr} not in database')
        if isinstance(self.right_expr, Expr):
            self.right_expr = self.right_expr.compile()
            self.right_expr = f'({self.right_expr})'
        elif isinstance(self.right_expr, Relation):
            if not self.right_expr.is_in_database():
                raise Exception(f'{self.right_expr} not in database')
        
    def compile(self):
        """Compile the Join to a SQL query"""
        condition = f'SELECT * FROM {self.left_expr} NATURAL JOIN (SELECT * FROM {self.right_expr})' 
        print(self.common_attributes)
        return condition    

class Rename(Expr):
    """ Class that represents the Rename in SPJRUD
        
        Attributes:
        ----------
        old_column_name : str

        new_column_name : str

        relation : Relation or Expr
            Relation on which the join is executed
    """
    def __init__(self, old_column_name, new_column_name, relation):
        super().__init__(relation)
        self.old_column_name = old_column_name
        self.new_column_name = new_column_name
       
    def verify(self):
        """ Checks if the operation is valid """
        if not self.old_column_name.is_in_database():
            raise Exception(f'{self.old_column_name} not in database')
        if self.new_column_name.is_in_database():
            raise Exception(f'{self.new_column_name} already in database')

    def compile(self):
        """Compile the Rename to a SQL query"""
        return f'ALTER TABLE {self.relation} RENAME COLUMN {self.old_column_name} to {self.new_column_name}'
    
class Union(Expr):
    """ Class that represents the Union in SPJRUD
        
        Attributes:
        ----------
        left_expr : Relation or Expr
            The left expression of the union

        right_expr : Relation or Expr
            The right expression of the union

    """
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

    def verify(self):
        """ Checks if the operation is valid """
        if self.left_expr.get_attributes() == self.right_expr.get_attributes():
            #Check that they have exactly the same sets of attributes
            if isinstance(self.left_expr, Expr):
                self.left_expr = self.left_expr.compile()
            if isinstance(self.right_expr, Expr):
                self.right_expr = self.right_expr.compile()
                self.right_expr = f'({self.right_expr})'
        else:
            raise Exception(f'{self.left_expr} do not have the same attributes as {self.right_expr}')

    def compile(self):
        """Compile the Union to a SQL query"""
        return f'SELECT * FROM {self.left_expr} UNION SELECT * FROM {self.right_expr}'
         
class Difference(Expr):
    """ Class that represents the Difference in SPJRUD
        
        Attributes:
        ----------
        left_expr : Relation or Expr
            The left expression of the Difference

        right_expr : Relation or Expr
            The right expression of the Difference
    """

    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

    def verify(self):
        """ Checks if the operation is valid """
        if self.left_expr.get_attributes() == self.right_expr.get_attributes():
            if isinstance(self.left_expr, Expr):
                self.left_expr = self.left_expr.compile()
            if isinstance(self.right_expr, Expr):
                self.right_expr = self.right_expr.compile()
                self.right_expr = f'({self.right_expr})'
        else:
            raise Exception(f'{self.left_expr} do not have the same attributes as {self.right_expr}')
    
    def compile(self):
        """Compile the Difference to a SQL query"""
        return f'SELECT * FROM {self.left_expr} EXCEPT SELECT * FROM {self.right_expr}'

  