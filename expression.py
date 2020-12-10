from general import *

class Expr():
    def __init__(self, relation):
        self.relation = relation
################################
#Comment this code

class Operation():
    def __init__(self, left_member, right_member):
        self.left_member = left_member
        self.right_member = right_member
        self.operator = None 

    def __str__(self):
        return f'{self.left_member} {self.operator} {self.right_member}'

class Cst():
    def __init__(self, value):
        self.value = value 

    def __str__(self):
        return f'"{self.value}"'

class Eq(Operation):
    def __init__(self, left_member, right_member):
        super().__init__(left_member, right_member)
        self.operator = "="
    
    def __str__(self):
        return super().__str__()

class Gt(Operation):
    """Greater than..."""
    def __init__(self, left_member, right_member):
        super().__init__(left_member, right_member)
        self.operator = ">"
    
    def __str__(self):
        return super().__str__()

class Gte(Operation):
    """Greater than..."""
    def __init__(self, left_member, right_member):
        super().__init__(left_member, right_member)
        self.operator = ">="
    
    def __str__(self):
        return super().__str__()

class St(Operation):
    """Greater than..."""
    def __init__(self, left_member, right_member):
        super().__init__(left_member, right_member)
        self.operator = "<"
    
    def __str__(self):
        return super().__str__()

class Ste(Operation):
    """Greater than..."""
    def __init__(self, left_member, right_member):
        super().__init__(left_member, right_member)
        self.operator = "<="
    
    def __str__(self):
        return super().__str__()

class Diff(Operation):
    def __init__(self, left_member, right_member):
        super().__init__( left_member, right_member)
        self.operator = '<>'

    def __str__(self):
        return super().__str__()

###############################

class Select(Expr):
    def __init__(self, operator, relation):
        super().__init__(relation)
        self.operator = operator

    def verify(self):
        if isinstance(self.operator, Expr): #Si operation est expression, operation.compile
            self.operator.compile()
        else:
            if isinstance(self.operator, Operation):
                if isinstance(self.operator.right_member, Cst):
                    if isinstance(self.operator.left_member, Cst):
                        #problem
                        pass
                    elif isinstance(self.operator.left_member, Column):
                        pass
        return True

    def compile(self):
        #Select(Eq('Country', '=', Cst('Mali')), Rel('CC'))
        if self.verify():
            condition = f'SELECT * FROM {self.relation} WHERE {self.operator}' 
            #print(condition) 
            return condition     
        else:
            pass
            #error                 

class Proj(Expr):
    def __init__(self, list_attributes, relation):
        super().__init__(relation)
        self.list_attributes = list_attributes

    def verify(self):
        if isinstance(self.relation, Expr):
            #self.relation = f'({self.relation})'
            self.relation = self.relation.compile()
        else:
            pass

    def compile(self):
        #Select('Country', '=', Cst('Mali'), Rel('CC'))
        self.verify()
        attributes = ''
        for i in range(len(self.list_attributes)):
            attributes += self.list_attributes[i]
            if i != (len(self.list_attributes) - 1):
                attributes += ", "
        condition = f'SELECT DISTINCT {attributes} FROM ({self.relation}) ' 
        return condition

class Join(Expr):
    pass

class Rename(Expr):
    pass

class Union(Expr):
    pass

class Difference(Expr):
    pass