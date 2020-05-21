from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime
from flask import flash

#Connect to DB (next 2)
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')
conn = engine.connect()

#Pass in arguments in order: In Game Name, Email, Password, DB Object of Users
def main(ign, email, password, users):
    x = 0
    if x == 0:
        flash("Account Created Successfully")
        s = users.insert().values(IGN = ign, Password = password, Email = email, RegistrationDate = datetime.now(), StorageCapacity = 10, StorageUsed = 0 )
        result = conn.execute(s)
        return True
    else:
        flash("Email in use.")
        return False

    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
