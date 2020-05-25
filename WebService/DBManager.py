from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
meta = MetaData()

#create engine for SQLAlchemy ORM
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')

items = Table(
    'items', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('MuleID', Integer),
    Column('GameID', String),
    Column('Owner', Integer),
    Column('InOffer', Integer, default=0)
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
    Column('type', Integer),
    Column('slot1', String),
    Column('slot2', String),
    Column('slot3', String),
    Column('slot4', String),
    Column('slot5', String),
    Column('slot6', String),
    Column('slot7', String),
    Column('slot8', String),
    Column('slot9', String),
    Column('slot10', String),
    Column('slot11', String),
    Column('slot12', String),
    Column('slot13', String),
    Column('slot14', String),
    Column('slot15', String),
    Column('slot16', String),
)

transactions = Table(
    'transactions', meta,
    Column('id', Integer, primary_key = True),
    Column('UserID', Integer),
    Column('MuleID', Integer),
    Column('MMID', Integer),
    #This will be the RotMG ID of the item the user gave
    Column('UserGave', String),
    #This will be the ROTMG ID of the item
    Column('UserRecieved', String),
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
    Column('Seeking', String),
    Column('SeekingQuantity', Integer),
    Column('Providing', String),
    Column('ProvidingQuantity', Integer),
    Column('Created', String),
    Column('Expiring', String),
    Column('Fulfilled', Integer),
    Column('FulfilledBy', Integer),
    Column('FulfilledWhen', String),
)

itemIds = Table(
    'itemIds', meta,
    Column('id', String),
    Column('Name', String)
)

withdraws = Table(
    'withdraws', meta,
    Column('id', Integer, primary_key = True),
    Column('muleID', Integer),
    Column('mmID', Integer),
    Column('recipient', String),
    Column('server', String),
    Column('status', String),
    Column('completed', Integer),
    Column('dateTimeInitialized', String),
    Column('expired', Integer),
)

deposits = Table(
    'deposits', meta,
    Column('id', Integer, primary_key = True),
    Column('muleID', Integer),
    Column('mmID', Integer),
    Column('IGN', String),
    Column('server', String),
    Column('status', String),
    Column('completed', Integer),
    Column('dateTimeInitialized', String),
    Column('expired', Integer),
    Column('deposited', String), #Just import comma seperated string of ids
)
#Table has been created. Will leave code above for reference. Note sure what the correct standards are for handling database itililization code.
meta.create_all(engine)


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
