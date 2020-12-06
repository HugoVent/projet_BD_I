import sqlite3 

#database = input("Sur quelle base de données souhaitez vous effectuer des requêtes SPJRUD ? \n")
database = 'test.db'
#Establish the connection with the database
conn = sqlite3.connect(database)
c = conn.cursor()


for row in c.execute("SELECT date FROM stocks WHERE trans = 'BUY'"):
    print(row)
# Save the changes
conn.commit()

conn.close()

class Select():
    def __init__(self, left, operator, right, relation):
        self.left = left
        self.operator = operator
        self.right = right
        self.relation = relation

    def verify(self):
        pass

    def compile(self):
        #Select('Country', '=', Cst('Mali'), Rel('CC'))
        condition = "SELECT * FROM" + str(self.relation) + "WHERE" + str(self.left) + str(self.operator) + str(self.right)
        print(condition)

            
class Proj():
    pass

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

test =  Select("A", "=", "1"0, "(R)")
test.compile()