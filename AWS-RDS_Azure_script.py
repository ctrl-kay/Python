import mysql.connector, random, string, time

### function to generate a random string of 50 characters ###
def generateString():
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(50))

### set host endpoints ###
azrhost = "azurelab1.mysql.database.azure.com"
rdshost = "rdslab2.cjd7xyafqouy.us-west-2.rds.amazonaws.com"

###### RDS SECTION ######

### connector ###
rdsDB = mysql.connector.connect(
	host=rdshost,
	user="kay",
	passwd="Password1"
)
### cursor ###
mycursor = rdsDB.cursor()

### select database ###
try:
	mycursor.execute("USE lab2db;")
	print("RDS: Using lab2db...")
except:
	print("RDS: Nope.")

### insert, update, query, delete loops ###
entries1 = []
start = time.time()
print("Performing insertions...")
for x in range(250):
	randString = generateString()
	entries1.append(randString)
	mycursor.execute("INSERT INTO testTable (field1, field2) VALUES (%s, %s)", (randString, "A"))
	rdsDB.commit()
print("Insertions complete.")
print("Performing updates...")
for x in range(250):
	randEntry = random.choice(entries1)
	mycursor.execute("UPDATE testTable SET field2 = 'B' WHERE field1 = %s", (randEntry,))
	rdsDB.commit()
print("Updates complete.")
print("Performing queries...")
for x in range(250):
	randEntry = random.choice(entries1)
	mycursor.execute("SELECT field2 FROM testTable WHERE field1 = %s", (randEntry,))
	mycursor.fetchone()
print("Queries complete.")
print("Performing deletions...")
for x in range(250):
	mycursor.execute("DELETE FROM testTable LIMIT 1")
	rdsDB.commit()
mycursor.close()
print("Deletions complete.")

### get task time ###
end = time.time()
totalTime = end - start
print("RDS task time: %d" %totalTime)

###### AZURE SECTION ######

### connector ###
azrDB = mysql.connector.connect(
	host=azrhost,
	user="kay@azurelab1",
	passwd="Password1"
)

### cursor ###
mycursor2 = azrDB.cursor()

### select db ###
try:
	mycursor2.execute("USE lab2db;")
	print("Azure: Using lab2db...")
except:
	print("Azure: Nope.")

### insert, update, query, delete loops ###
start2 = time.time()
entries2 = []
print("Performing insertions...")
for x in range(250):
    randString2 = generateString()
    entries2.append(randString2)
    mycursor2.execute("INSERT INTO testTable (field1, field2) VALUES (%s, %s)", (randString2, "A"))
    azrDB.commit()
print("Insertions complete.")
print("Performing updates...")
for x in range(250):
    randEntry2 = random.choice(entries2)
    mycursor2.execute("UPDATE testTable SET field2 = 'B' WHERE field1 = %s", (randEntry2,))
    azrDB.commit()
print("Updates complete.")
print("Performing queries...")
for x in range(250):
	randEntry = random.choice(entries2)
	mycursor2.execute("SELECT field2 FROM testTable WHERE field1 = %s", (randEntry2,))
	mycursor2.fetchone()
print("Queries complete.")
print("Performing deletions...")
for x in range(250):
   mycursor2.execute("DELETE FROM testTable LIMIT 1")
   azrDB.commit()
mycursor2.close()	
print("Deletions complete.")

### get task time ###
end2 = time.time()
totalTime2 = end2 - start2
print("Azure task time: %d" %totalTime2)

