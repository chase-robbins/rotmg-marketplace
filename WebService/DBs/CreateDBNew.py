from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
meta = MetaData()

#create engine for SQLAlchemy ORM
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres', echo = True)

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
    Column('id', Integer, prmiary_key = True),
    Column('UserID', Integer),
    Column('MuleID', Integer),
    Column('MMID', Integer),
    #This will be our ID of the item the user gave
    Column('UserGave', Integer),
    #This will be the ROTMG ID of the item
    Column('UserRecieved', Integer),
    Column('DateTime', Integer),
)

users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('IGN', String),
    Column('Password', String),
    Column('Email', String),
    Column('RegistrationDate', Integer),
)


meta.create_all(engine)
ins = items.insert(), [
    {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Defence', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Dexterity', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Wisdom', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214}, ]


conn = engine.connect()
result = conn.execute(items.insert(), [
    {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Defence', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Dexterity', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Wisdom', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    {'name' : 'Potion of Life', 'MuleID' : 123, 'GameID' : 1234, 'Owner' : 214},
    ])
