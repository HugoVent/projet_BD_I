import general

class Proj():
    def __init__(self, left, right, relation):
        self.left = left
   
        self.right = right
        self.relation = relation

    def verify(self):
        pass

    def compile(self):
        #Select('Country', '=', Cst('Mali'), Rel('CC'))
        condition = "SELECT " + str(self.left) + " FROM " + str(self.relation)
        return condition