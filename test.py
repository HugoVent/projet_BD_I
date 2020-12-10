#
# 
# import pytest
from expression import *
from general import *

#Test the table
database = Database('/Users/hugo/Documents/pgm/hugo_dev/BAB2/DB/prj_spjrud2sql/project.db')
cursor = database.get_cursor()

#Get all tables
cursor.execute('SELECT name from sqlite_master where type= "table"')
print(cursor.fetchall())

table = Relation(cursor, "id")
"""
  def readSqliteTable(self):
        print("Printing each row")
        for row in self.table:
            print(row[0])
"""
#Test the constant and see if the constant print well
constant1 = Cst("hello")
print(constant1)

#Test the equality
equal = Eq("name", Cst("World"))
select = Select(equal, table)
print(select.compile())

#Test the "greater than"

#Test the Proj
def test_proj():
    assert 1 + 1 == 3
    #assert Proj(["name", "surname"], select) == "Oui"
proj = Proj(["name", "surname"], select)
print(proj.compile())
