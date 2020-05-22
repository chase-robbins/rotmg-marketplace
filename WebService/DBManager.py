from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
meta = MetaData()

#create engine for SQLAlchemy ORM
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')

items = Table(
    'items', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('MuleID', Integer),
    Column('GameID', Integer),
    Column('Owner', Integer),
)

middleMen = Table(
    'middleMen', meta,
    Column('id', Integer, primary_key = True),
    Column('IGN', String),
    Column('Email', String),
    Column('Password', String),
    Column('bdayMonth', Integer),
    Column('bdayDay', Integer),
    Column('bdayYear', Integer),
)

mules = Table(
    'mules', meta,
    Column('id', Integer, primary_key = True),
    Column('IGN', String),
    Column('Email', String),
    Column('Password', String),
    Column('bdayMonth', Integer),
    Column('bdayDay', Integer),
    Column('bdayYear', Integer),
    Column('slot1', Integer),
    Column('slot2', Integer),
    Column('slot3', Integer),
    Column('slot4', Integer),
    Column('slot5', Integer),
    Column('slot6', Integer),
    Column('slot7', Integer),
    Column('slot8', Integer),
    Column('slot9', Integer),
    Column('slot10', Integer),
    Column('slot11', Integer),
    Column('slot12', Integer),
    Column('slot13', Integer),
    Column('slot14', Integer),
    Column('slot15', Integer),
    Column('slot16', Integer),
)

transactions = Table(
    'transactions', meta,
    Column('id', Integer, primary_key = True),
    Column('UserID', Integer),
    Column('MuleID', Integer),
    Column('MMID', Integer),
    #This will be our ID of the item the user gave
    Column('UserGave', Integer),
    #This will be the ROTMG ID of the item
    Column('UserRecieved', Integer),
    Column('DateTime', String),
)

users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('IGN', String),
    Column('Password', String),
    Column('Email', String),
    Column('RegistrationDate', String),
    Column('StorageCapacity', Integer),
    Column('StorageUsed', Integer),
    Column('Verified', Integer),
)

offers = Table(
    'offers', meta,
    Column('id', Integer, primary_key = True),
    Column('Owner', Integer),
    Column('Seeking', Integer),
    Column('SeekingQuantity', Integer),
    Column('Providing', Integer),
    Column('ProvidingQuantity', Integer),
    Column('Created', String),
    Column('Expiring', String),
    Column('Fulfilled', Integer),
    Column('FulfilledBy', Integer),
    Column('FulfilledWhen', String),
)
#Table has been created. Will leave code above for reference. Note sure what the correct standards are for handling database itililization code.
meta.create_all(engine)

# This block of code will insert these items into the database in dictionary form.
#
# conn = engine.connect()
# result = conn.execute(items.insert(), [
#     {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
#     {'name' : 'Potion of Defence', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
#     {'name' : 'Potion of Dexterity', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
#     {'name' : 'Potion of Wisdom', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
#     {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
#     ])

conn = engine.connect()
s = items.select()
result = conn.execute(s)

row = result.fetchone()

for row in result:
    print (row)

# Script to search for life pots
# print("Searching through database to locate life pots...")
# s = items.select().where(items.c.name == "Potion of Life")
# result = conn.execute(s)
#
# for row in result:
#     print (row)

#TransactionArray = ["Hello world.", "Dog"]
