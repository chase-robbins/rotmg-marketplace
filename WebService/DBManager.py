from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()
meta = MetaData()

#create engine for SQLAlchemy ORM
engine = create_engine('postgresql://postgres:testingPassword@localhost:5432/postgres')


session = Session(bind=engine)

def DropAll():
    Base.metadata.drop_all(engine)

items = Table(
    'items', meta,
    Column('id', Integer, primary_key = True),
    Column('muleID', Integer),
    Column('gameId', String),
    Column('owner', Integer),
    Column('inOffer', Integer, default=0),
    Column('slot', Integer)
)

mules = Table(
    'mules', meta,
    Column('id', Integer, primary_key = True),
    Column('ign', String),
    Column('email', String),
    Column('password', String),
    Column('bdayDay', Integer),
    Column('bdayMonth', Integer),
    Column('bdayYear', Integer),
    Column('isBanned', Boolean),
    Column('type', Integer),
)

transactions = Table(
    'transactions', meta,
    Column('id', Integer, primary_key = True),
    Column('user1', Integer),
    Column('user2', Integer),
    Column('user1Gave', String),
    Column('user2Gave', String),
)

users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('ign', String),
    Column('password', String),
    Column('email', String),
    Column('registrationDate', String),
    Column('storageCapacity', Integer),
    Column('storageUsed', Integer),
    Column('verificationString', String),
    Column('verified', Boolean, default = False),
    Column('tier', Integer),
)

offers = Table(
    'offers', meta,
    Column('id', Integer, primary_key = True),
    Column('owner', Integer),
    Column('created', String),
    Column('expiring', String),
    Column('fulfilled', Boolean),
    Column('fulfilledBy', String),
    Column('fulfilledDate', String),
)

offer_data = Table(
    'offer_data', meta,
    Column('id', Integer),
    Column('seeking', ARRAY(String)),
    Column('providing', ARRAY(String)),
    Column('id', Integer, primary_key = True),

)

itemIds = Table(
    'itemIds', meta,
    Column('id', String, primary_key = True),
    Column('Name', String),
)

withdraws = Table(
    'withdraws', meta,
    Column('id', Integer, primary_key = True),
    Column('mmID', Integer),
    Column('recipient', String),
    Column('server', String),
    Column('status', String),
    Column('completed', Integer),
    Column('dateTimeInitialized', String),
    Column('expired', Integer),
)

withdrawnItems = Table(
    'withdrawnItems', meta,
    Column('withdrawID', Integer),
    Column('itemIds', ARRAY(Integer, dimensions=1)),
)

deposits = Table(
    'deposits', meta,
    Column('id', Integer, primary_key = True),
    Column('mmID', Integer),
    Column('IGN', String),
    Column('server', String),
    Column('status', String),
    Column('completed', Integer),
    Column('dateTimeInitialized', String),
    Column('expired', Integer),
)

depositedItems = Table(
    'depositedItems', meta,
    Column('depositId', Integer),
    Column('items', ARRAY(Integer, dimensions=2)),
    Column('id', Integer, primary_key = True),
)

servers = Table(
    'servers', meta,
    Column('id', Integer, primary_key = True),
    Column('ip', String),
    Column('name', String)
)

proxys = Table(
    'proxys', meta,
    Column('id', Integer, primary_key = True),
    Column('ip', String),
    Column('port', Integer),
    Column('username', String),
    Column('password', String),
    Column('dateAdded', String),
    Column('expired', String)
)
#Table has been created. Will leave code above for reference. Note sure what the correct standards are for handling database itililization code.
meta.create_all(engine)

# Script to search for life pots
# print("Searching through database to locate life pots...")
# s = items.select().where(items.c.name == "Potion of Life")
# result = conn.execute(s)
#
# for row in result:
#     print (row)

#TransactionArray = ["Hello world.", "Dog"]
