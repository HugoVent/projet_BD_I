import sqlite3 
from utility import *
#database = input("Sur quelle base de données souhaitez vous effectuer des requêtes SPJRUD ? \n")
#database = 'project.db'
#Establish the connection with the database
conn = sqlite3.connect("/Users/hugo/Documents/School/pgm/hugo_dev/BAB2/DB/prj_spjrud2sql/project.db")
c = conn.cursor()


class Select(Expr):
    def __init__(self, left, operator, right, relation):
        super().__init__(relation)
        self.left = left
        self.operator = operator
        self.right = right

    def compile(self):
        #Select('Country', '=', Cst('Mali'), Rel('CC'))
        condition = "SELECT * FROM " + str(self.relation) + " WHERE " + str(self.left) + " " + str(self.operator) + " " +str(self.right)
        return condition
            
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

class Join():
    pass

class Rename():
    pass

class Union():
    pass

class Difference():
    pass

class Cst():
    pass  

class Operation():
    pass


#Proj(['Population], Join(Rename('Name, Capital, Rel('Cities)), Select(Eq('Country', Cst('Mali')), Rel('CC'))))    

###############################################################################################

test = Proj("name", '"Hugo"' , "id")
#test.compile()
#c.execute()
request = test.compile()
print(request)
c.execute("SELECT * FROM id")
for row in c.execute(request) :
    print(row)
#for row in c.execute("SELECT date FROM stocks WHERE trans = 'BUY'"):
    #print(row)
# Save the changes
conn.commit()

conn.close()