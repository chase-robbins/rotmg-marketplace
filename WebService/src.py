from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, and_
import DBManager
import InitiateTransaction
import listOffers
import createAccount
import pwSalting
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy import func

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

#get the name of an item from the GameID number
def getItemName(id):
    print(id)
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.id == str(id))
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return ""
    else:
        return row[1]
#returns the Jinja2 syntax to get the icon for an item
def getItemImage(id):
    return "\"{{ url_for('static', filename='items/" + id + ".png') }}\""

#returns an object containing the active offers from a given UID
def getActiveOffers(id):
    # s = DBManager.offers.select().where(and_(DBManager.offers.c.owner == id, DBManager.offers.c.Fulfilled != 1))
    s = DBManager.offers.select().where(DBManager.offers.c.owner == id)
    result = conn.execute(s)
    return result

#returns an object containing all items stored in DB
def getAllItems():
        s = DBManager.itemIds.select()
        result = conn.execute(s)
        return result.fetchall()

#returns the item capacity given a UID
def getCapacity(UID):
    s = DBManager.users.select().where(DBManager.users.c.id == UID)
    result = conn.execute(s).fetchone()
    return result[5]

#list the items of a player given their UID
def listItemsFromUID(UID):
    s = DBManager.items.select().where(DBManager.items.c.owner == UID)
    result = conn.execute(s)
    return result

def getItemsForInventory(UID):
    ## QUESTION: import pdb; pdb.set_trace()
    var = DBManager.session.query(
        DBManager.items.columns.gameId,
        func.count(DBManager.items.columns.gameId)
        ).group_by(DBManager.items.columns.gameId).filter(DBManager.items.c.owner == UID).all()
    print(var)
    return var

def getInvUsed(UID):
    s = DBManager.items.select().where(DBManager.items.c.owner == UID)
    result = conn.execute(s)
    return len(result.fetchall())

def createOffer(UID, seeking, providing):
    end_date = datetime.now() + timedelta(days=1)
    s = DBManager.offers.insert().values(owner = UID, created = datetime.now(), expiring = end_date, fulfilled = False, fulfilledBy = None, fulfilledDate = None)
    result = conn.execute(s)
    s = DBManager.offer_data.insert().values(id = result.inserted_primary_key[0], seeking = seeking, providing = providing)
    result = conn.execute(s)

def getItemID(str):
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.Name == str)
    result = conn.execute(s)
    return result.fetchone()[0]
# def parseOffer(offerId):
