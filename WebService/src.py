from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, and_
import DBManager
import InitiateTransaction
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
    s = DBManager.offers.select()
    result = conn.execute(s)
    return result

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
    s = DBManager.offer_data.select()
    result = conn.execute(s)
    newList = []
    for item in result:
        if str in item[1]:
            newList.append(item)
    return newList

def searchOffers(itemId):
    s = DBManager.offer_data.select()
    result = conn.execute(s).fetchall()
    print(result)
    for item in result:
        itemisthere = False
        seekingObj = item[1]
        for lilPart in seekingObj:
            if str(itemId) in lilPart:
                itemisthere = True
        if itemisthere == False:
            result.remove(item)
    print(result)
    return result

#get the name of an item from the GameID number
def getItemName(id):
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
    s = DBManager.offers.select().where(DBManager.offers.c.owner == id)
    result = conn.execute(s).fetchall()
    ids = []
    for item in result:
        ids.append(item[0])
    offers = []
    for id in ids:
        s = DBManager.offer_data.select().where(DBManager.offer_data.c.id == id)
        result = conn.execute(s).fetchone()
        buying = result[1]
        selling = result[2]
        offers.append([id, buying,selling])
    return offers

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

#returns the object necessary for rendering inventory
def getItemsForInventory(UID):
    ## QUESTION: import pdb; pdb.set_trace()
    var = DBManager.session.query(
        DBManager.items.columns.gameId,
        func.count(DBManager.items.columns.gameId)
        ).group_by(DBManager.items.columns.gameId).filter(DBManager.items.c.owner == UID).all()
    return var

#returns an int describing how much of the user's inventory has been used
def getInvUsed(UID):
    s = DBManager.items.select().where(DBManager.items.c.owner == UID)
    result = conn.execute(s)
    return len(result.fetchall())

#creates offers
def createOffer(UID, seeking, providing):
    #CHECK THAT THE USER HAS THE ITEMS REQUESTED:
    for item in providing:
        list = item.split('x')
        quantity = int(list[0])
        itemId = list[1]
        s = DBManager.items.select().where(
            and_(
                DBManager.items.c.owner == UID,
                DBManager.items.c.gameId == itemId,
                DBManager.items.c.inOffer == 0
            )
        )
        result = conn.execute(s).fetchall()
        if quantity > len(result):
            return "You do not have the items you have attempted to sell."
    end_date = datetime.now() + timedelta(days=1)
    s = DBManager.offers.insert().values(owner = UID, created = datetime.now(), expiring = end_date, fulfilled = False, fulfilledBy = None, fulfilledDate = None)
    result = conn.execute(s)
    s = DBManager.offer_data.insert().values(id = result.inserted_primary_key[0], seeking = seeking, providing = providing)
    result = conn.execute(s)
    print(providing)
    return "Success"

def getItemID(str):
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.Name == str)
    result = conn.execute(s)
    return result.fetchone()[0]

def parseOffer(str):
    arr = []
    arr.append(str.split('x',1)[0])
    arr.append(str.split('x',1)[1])
    return arr

def getOfferData(offerId):
    buying = []
    selling = []
    s = DBManager.offer_data.select().where(DBManager.offer_data.c.id == offerId)
    result = conn.execute(s).fetchall()
    for object in result:
        buying.append(object[1])
        selling.append(object[2])
    finalObject = []
    finalObject.append(buying)
    finalObject.append(selling)
    return finalObject
