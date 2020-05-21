from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime

#Connect to DB (next 2)
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')
conn = engine.connect()

#Pass in arguments in order: In Game Name, Email, Password, DB Object of Users
def main(ign, email, password, users):
    s = users.insert().values(IGN = ign, Password = password, Email = email, RegistrationDate = datetime.now(), StorageCapacity = 10, StorageUsed = 0 )
    result = conn.execute(s)
    print("Account created.")

    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
