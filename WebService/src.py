from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, and_
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
    s = DBManager.users.select().where(DBManager.users.c.email == email)
    result = conn.execute(s)
    row = result.fetchone()
    while row:
        uid = row[0]
        return uid
    return 0

#Login Function
def tryLogin(email, password):
    s = DBManager.users.select().where(DBManager.users.c.email == email)
    result = conn.execute(s)
    row = result.fetchone()
    while row:
        pw = row[2]
        if pwSalting.verify_password(pw, password):
            return True
        else:
            flash("Password Incorrect")
            return False
    else:
        flash("Account not found. Was there a typo in your email?")
        return False

#Function to test Deposits
def testDeposit(itemID, UID):
    s = DBManager.items.insert().values(owner = UID, gameId = itemID)
    result = conn.execute(s)

#list the items of a player given their UID
def listItemsFromUID(UID):
    s = DBManager.items.select().where(DBManager.items.c.owner == UID)
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
        if str in item[1]:
            newList.append(item)
    return newList

def getItemName(id):
    print(id)
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.id == str(id))
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return ""
    else:
        return row[1]

def getItemImage(id):
    return "\"{{ url_for('static', filename='items/" + id + ".png') }}\""

def getActiveOffers(id):
    # s = DBManager.offers.select().where(and_(DBManager.offers.c.owner == id, DBManager.offers.c.Fulfilled != 1))
    s = DBManager.offers.select().where(DBManager.offers.c.owner == id)
    result = conn.execute(s)
    return result

def withdraw(itemid, userid):
        s = DBManager.items.select().where(DBManager.items.c.owner == str(userid))
        result = conn.execute(s)
        print(result.fetchall())

def getAllItems():
        s = DBManager.itemIds.select()
        result = conn.execute(s)
        return result.fetchall()

def getCapacity(UID):
    s = DBManager.users.select().where(DBManager.users.c.id == UID)
    result = conn.execute(s).fetchone()
    return result[5]


#create test offer
# def createTestOffer(seeking, seekingq, providing, providingq, uid):
#     s = DBManager.offers.insert().values(owner = uid, seeking = seeking, SeekingQuantity = seekingq, Providing = providing, ProvidingQuantity = providingq, Created = datetime.now())
#     result = conn.execute(s)
