import mysql.connector, random, string, time, psycopg2

### function to generate a random string of 50 characters ###
def generateString():
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(50))

### set host endpoints ###
sqlhost = "cosc417.mysql.database.azure.com"
posthost = "cosc417p.postgres.database.azure.com"


###### MySQL SECTION ######

### connector ###
sqlDB = mysql.connector.connect(
	host=sqlhost,
	user="kay@cosc417",
	passwd="Password1"
)

### cursor ###
mycursor2 = sqlDB.cursor()

### select db ###
try:
	mycursor2.execute("USE lab2db;")
	print("MySQL: Using lab2db...")
except:
	print("MySQL: Nope.")

### insert, update, query, delete loops ###
start2 = time.time()
entries2 = []
print("MYSQL Performing insertions...")
for x in range(250):
    randString2 = generateString()
    entries2.append(randString2)
    mycursor2.execute("INSERT INTO testTable (field1, field2) VALUES (%s, %s)", (randString2, "A"))
    sqlDB.commit()
print("Insertions complete.")
print("MYSQL Performing updates...")
for x in range(250):
    randEntry2 = random.choice(entries2)
    mycursor2.execute("UPDATE testTable SET field2 = 'B' WHERE field1 = %s", (randEntry2,))
    sqlDB.commit()
print("Updates complete.")
print("MYSQL Performing queries...")
for x in range(250):
	randEntry = random.choice(entries2)
	mycursor2.execute("SELECT field2 FROM testTable WHERE field1 = %s", (randEntry2,))
	mycursor2.fetchone()
print("Queries complete.")
print("MYSQL Performing deletions...")
for x in range(250):
   mycursor2.execute("DELETE FROM testTable LIMIT 1")
   sqlDB.commit()
mycursor2.close()	
print("Deletions complete.")

### get task time ###
end2 = time.time()
totalTime2 = end2 - start2
print("MySQL task time: %d" %totalTime2)


###### Postgres SECTION ######

### connector ###
postDB = psycopg2.connect(
	host=posthost,
	user="kay@cosc417p",
	password="Password1",
	database="postgres"
)

### cursor ###
mycursor = postDB.cursor()

### select db ###
#try:
#	mycursor.execute("USE public;")
#	print("Postgres: Using public DB...")
#except:
#	print("Postgres: Nope.")

### insert, update, query, delete loops ###
start = time.time()
entries = []
print("Postgres performing insertions...")
for x in range(250):
    randString = generateString()
    entries.append(randString)
    mycursor.execute("INSERT INTO testTable (field1, field2) VALUES (%s, %s)", (randString, "A"))
    postDB.commit()
print("Insertions complete.")
print("Postgres performing updates...")
for x in range(250):
    randEntry = random.choice(entries)
    mycursor.execute("UPDATE testTable SET field2 = 'B' WHERE field1 = %s", (randEntry,))
    postDB.commit()
print("Updates complete.")
print("Postgres performing queries...")
for x in range(250):
	randEntry = random.choice(entries)
	mycursor.execute("SELECT field2 FROM testTable WHERE field1 = %s", (randEntry,))
	mycursor.fetchone()
print("Queries complete.")
print("Postgres performing deletions...")
for x in range(250):
   mycursor.execute("DELETE FROM testTable WHERE field1 IN (SELECT field1 FROM testTable WHERE field2='B' LIMIT 1)") 
   postDB.commit()
mycursor.close()	
print("Deletions complete.")

### get task time ###
end = time.time()
totalTime = end - start
print("Postgres task time: %d" %totalTime)

