import ast

class Expression:
    def __init__(self):
        pass
    
    def validation(self):
        pass

    def compilation(self):
        pass

class Select(Expression):
    pass  

class Proj(Expression):
    pass

class Join(Expression):
    pass

class Rename(Expression):
    pass

class Union(Expression):
    pass

class Difference(Expression):
    pass

class Cst(Expression):
    pass  

class Operation(Expression):
    pass


#Proj(['Population], Join(Rename('Name, Capital, Rel('Cities)), Select(Eq('Country', Cst('Mali')), Rel('CC'))))    
