import psycopg2
from sqlalchemy import create_engine

#create engine for SQLAlchemy ORM
engine = create_engine('postgresql://postgres:testingPassword@maik8.de/postgres')

#Setting credentials and creating a connect object to the database.
myConnection = psycopg2.connect( host="localhost", user="postgres", password="testingPassword", dbname="postgres" )

#creating a cursor object from our connection
cursor = myConnection.cursor()

#Printing connection parameters
print( myConnection.get_dsn_parameters(), "\n")


createTableQuery = '''CREATE TABLE items
    ("ID"	SERIAL,
    "Name"	TEXT,
    "MuleID"	INTEGER,
    "GameID"	INTEGER,
    PRIMARY KEY("ID"));'''

#cursor.execute(createTableQuery)

insertQuery = '''INSERT INTO items ("Name", "MuleID", "GameID")
                VALUES (%s, %s, %s)'''

recordToInsert = ("Chase", 202, 303)
#cursor.execute(insertQuery, recordToInsert)

cursor.execute("DELETE FROM items WHERE Name=%s", ("Chase",))
myConnection.commit()

cursor.execute('SELECT * from items')

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
myConnection.close()
