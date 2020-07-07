from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres', echo = True)
meta = MetaData()

ins = items.insert().values(name = 'Potion of Life', MuleID = 123, GameID = 1234, Owner = 214)
conn = engine.connect()
result = conn.execute(ins)
