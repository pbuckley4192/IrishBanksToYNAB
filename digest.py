import csv
import sqlite3

# Open CSV File
file = open('statement.csv', mode='r')
csv_file = csv.DictReader(file)

# Open DB
conn = sqlite3.connect('data.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (date text, type text,contactless bool, trans text, change real, balance real)''')

# Parse out the statment
for row in csv_file:
	descript=""
	contact="False"
	if str(row[" Type"]).startswith("POS"):
		subs = str(row[" Description"]).split(",", 1)
		descript = subs[1].lstrip()
		contact =str(str(subs[0]).endswith("C "))
		
	else:
		descript = row[" Description"].lstrip()

	# Insert a row of data
	c.execute("INSERT INTO transactions VALUES (\""+row['Date']+"\",\""+ row[' Type']+"\",\""+contact+"\",\""+ descript +"\","+ row[' Value'] +","+ row[' Balance'] + ")")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
