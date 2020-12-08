from general import *

class Select(Expr):
    def __init__(self, operation, relation):
        super().__init__(relation)
        self.operation = operation

    def verify(self):
        if isinstance(self.operation.right_member, Cst):
            pass #vérifier les types


    def compile(self):
        #Select(Eq('Country', '=', Cst('Mali')), Rel('CC'))
        condition = "SELECT * FROM " + str(self.relation) + " WHERE " + str(self.operation)
        return condition

        