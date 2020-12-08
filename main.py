import sqlite3 
conn = sqlite3.connect('/Users/hugo/Documents/School/pgm/hugo_dev/BAB2/DB/prj_spjrud2sql/project.db')
c = conn.cursor()

# Create table
#c.execute('''CREATE TABLE id
 #            (name text, familyName text)''')

# Insert a row of data
c.execute("INSERT INTO id VALUES ('Hugo', 'Venturoso')")

# Just a simple test 
for row in c.execute("SELECT * FROM id") :
    print(row)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
