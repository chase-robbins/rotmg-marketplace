from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import DBManager
import InitiateTransaction
import listOffers
import createAccount
import pwSalting
from flask import flash
from datetime import datetime

#Connect to Database
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')
conn = engine.connect()

#Function to list items in database
def listTheOffers():
    return listOffers.main(DBManager.offers)

#Function that creates an account
def createAcc(ign, email, password):
    return createAccount.main(ign, email, password, DBManager.users)

#Function that returns the UID of a certain IGN
def getUID(email):
    s = DBManager.users.select().where(DBManager.users.c.Email == email)
    result = conn.execute(s)
    row = result.fetchone()
    while row:
        uid = row[0]
        return uid
    return 0

#Login Function
def tryLogin(email, password):
    s = DBManager.users.select().where(DBManager.users.c.Email == email)
    result = conn.execute(s)
    row = result.fetchone()
    while row:
        pw = row[2]
        if pwSalting.verify_password(pw, password):
            print("Verification Successful")
            return True
        else:
            flash("Password Incorrect")
            print("Verification NOT Successful")
            return False
    else:
        flash("Account not found. Was there a typo in your email?")
        return False

#Function to test Deposits
def testDeposit(itemID, UID):
    s = DBManager.items.insert().values(Owner = UID, GameID = itemID)
    result = conn.execute(s)

#list the items of a player given their UID
def listItemsFromUID(UID):
    s = DBManager.items.select().where(DBManager.items.c.Owner == UID)
    result = conn.execute(s)
    return result

#return the in game name of a user given their UID
def getIGN(UID):
    s = DBManager.users.select().where(DBManager.users.c.id == UID)
    result = conn.execute(s)
    return result.fetchone()[1]

#search within inventory for string
def invSearch(str, UID):
    s = DBManager.items.select().where(DBManager.users.c.id == UID)
    result = conn.execute(s)
    newList = []
    for item in result:
        print("Item: " + item[1])
        if str in item[1]:
            print("Item contains target string.")
            newList.append(item)
    print(newList)
    return newList

def getItemName(id):
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.id == id)
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return ""
    else:
        row = result.fetchone()
        print(row['Name'])
        return row
#create test offer
def createTestOffer(seeking, seekingq, providing, providingq, uid):
    s = DBManager.offers.insert().values(Owner = uid, Seeking = seeking, SeekingQuantity = seekingq, Providing = providing, ProvidingQuantity = providingq, Created = datetime.now())
    result = conn.execute(s)
