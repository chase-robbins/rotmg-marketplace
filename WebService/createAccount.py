from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime
from flask import flash
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
import pwSalting
import random

#Connect to DB (next 2)
engine = create_engine('postgresql://postgres:testingPassword@maik8.de/postgres')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
#Pass in arguments in order: In Game Name, Email, Password, DB Object of Users
def main(ign, email, password, users):
    print("Attempting to create account:")
    print("ign: " + ign)
    print("email: " + email)
    print("password: " + password)
    verificationString = str(random.randint(1000,9999))
    #Check Email Not Used Before First
    if session.query(users).filter_by(email=email).count() > 0:
        flash("Email in use.")
        return False
    else:
        #To check that the ingame name has not been used before.
        if session.query(users).filter_by(ign=ign, verified=1).count() == 0:
            if len(password) > 7:
                flash("Account Created Successfully")
                s = users.insert().values(ign = ign, password = pwSalting.hash_password(password), email = email, registrationDate = datetime.now(), storageCapacity = 10, storageUsed = 0, verificationString = verificationString, tier = 1)
                result = conn.execute(s)
                return True
            else:
                flash("Password must be at least 8 characters.")
                return False
        else:
            flash("In game name already associated with another account. If this is a mistake, contact our staff on discord.")
            return False
    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
