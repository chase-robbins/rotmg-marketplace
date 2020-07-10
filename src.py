from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, and_
import DBManager
import InitiateTransaction
import createAccount
import pwSalting
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy import func
import env

#Connect to Database
engine = create_engine('postgresql://'+env.db_user+':'+env.db_pass+'@'+env.db_url+':'+env.db_port+'/'+env.db_name)\

conn = engine.connect()

#Function to list items in database
def listTheOffers():
    s = DBManager.offers.select().where(DBManager.offers.c.fulfilled == False)
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
    for item in result:
        itemisthere = False
        seekingObj = item[1]
        for lilPart in seekingObj:
            if str(itemId) in lilPart:
                itemisthere = True
        if itemisthere == False:
            result.remove(item)
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
    s = DBManager.offers.select().where(and_(DBManager.offers.c.owner == id, DBManager.offers.c.fulfilled == False))
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
        else:
            s = DBManager.items.update().where(
                and_(
                    DBManager.items.c.owner == UID,
                    DBManager.items.c.gameId == itemId,
                    DBManager.items.c.inOffer == 0
                )
            ).values(inOffer = 1)
    end_date = datetime.now() + timedelta(days=1)
    s = DBManager.offers.insert().values(owner = UID, created = datetime.now(), expiring = end_date, fulfilled = False, fulfilledBy = None, fulfilledDate = None)
    result = conn.execute(s)
    s = DBManager.offer_data.insert().values(id = result.inserted_primary_key[0], seeking = seeking, providing = providing)
    result = conn.execute(s)
    return "Success"

#gets the id of an item from it's Name
def getItemID(str):
    s = DBManager.itemIds.select().where(DBManager.itemIds.c.Name == str)
    result = conn.execute(s)
    return result.fetchone()[0]

#parses a string of quantityxname and returns an array [quantity, name]
def parseOffer(str):
    arr = []
    arr.append(str.split('x',1)[0])
    arr.append(str.split('x',1)[1])
    return arr

#returns an multidimensional array of offers from the ID of the offer
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

#returns the owner String name from the id of an offer
def getOfferOwner(offerId):
    s = DBManager.offers.select().where(DBManager.offers.c.id == offerId)
    result = conn.execute(s).fetchone()
    ownerId = result[1]
    s = DBManager.users.select().where(DBManager.users.c.id == ownerId)
    result = conn.execute(s).fetchone()
    return result[1]

#returns the account id that owns an offer from the offer id
def getOfferOwnerId(offerId):
    s = DBManager.offers.select().where(DBManager.offers.c.id == offerId)
    result = conn.execute(s).fetchone()
    return result[1]

#accepting offer logic and moving items from account to account
def acceptOffer(id, UID):

    s = DBManager.offers.select().where(DBManager.offers.c.id == id)
    result = conn.execute(s).fetchone()
    if len(result) == 0:
        return "This offer no longer exists."
    if result[4] == True:
        return "Offer has already been claimed by another user. Sorry!"

    #Generate a list of items required to fulfill the offer
    s = DBManager.offer_data.select().where(DBManager.offer_data.c.id == id)
    result = conn.execute(s).fetchone()
    neededItems = []
    for itemQuantityArray in result[1]:
        parseOfferObj = parseOffer(itemQuantityArray)
        i = parseOfferObj[0]
        x=0
        while x < int(i):
            neededItems.append(parseOfferObj[1])
            x+=1
    print("neededitems1:")
    print(neededItems)

    #Generate a list of items in the inventory of the user trying to fulfill the offer
    s = DBManager.items.select().where(DBManager.items.c.owner == UID)
    result = conn.execute(s).fetchall()
    userHas = []
    for item in result:
        userHas.append(item[2])

    #Compare the two, removing items once they're checked to account for reapeating items
    approved = False
    neededItemsDupe = []
    for item in neededItems:
        neededItemsDupe.append(item)
    for item in neededItemsDupe:
        isFound = False
        for item2 in userHas:
            if item2 == item:
                userHas.remove(item2)
                neededItemsDupe.remove(item2)
                isFound = True
        if isFound == False:
            return "" + getItemName(item) + " not found in your inventory. Transaction failed."
        else:
            approved = True

    #If all goes well, reassign owners of required items.
    if approved == True:
        offerOwner = getOfferOwnerId(id)
        #Take needed items from acceptor and reassign ownership:
        print("Trade approved")
        print(neededItems)
        for item in neededItems:
            s = DBManager.items.select().where(and_(DBManager.items.c.owner == UID, DBManager.items.c.gameId == item))
            result = conn.execute(s).fetchone()
            rowID = result[0]
            s = DBManager.items.update().where(DBManager.items.c.id == rowID).values(owner = offerOwner)
            conn.execute(s)

        #Take needed items from offer poster and reassign ownership
        providingItems = []
        s = DBManager.offer_data.select().where(DBManager.offer_data.c.id == id)
        result = conn.execute(s).fetchone()
        for itemQuantityArray in result[2]:
            parseOfferObj = parseOffer(itemQuantityArray)
            i = parseOfferObj[0]
            x=0
            while x < int(i):
                providingItems.append(parseOfferObj[1])
                x+=1
        for item in providingItems:
            s = DBManager.items.select().where(and_(DBManager.items.c.owner == offerOwner, DBManager.items.c.gameId == item))
            result = conn.execute(s).fetchone()
            rowID = result[0]
            s = DBManager.items.update().where(DBManager.items.c.id == rowID).values(owner = UID)
            conn.execute(s)

        #Set as fulfilled
        s = DBManager.offers.update().where(DBManager.offers.c.id == id).values(fulfilled = True, fulfilledBy = UID, fulfilledDate = datetime.now())
        conn.execute(s)
        return "Transaction Complete."
    else:
        return "Error"

#checks if a player can delete an offer and if so deletes it from the UID and offer id
def deleteOffer(id, UID):
    s = DBManager.offers.select().where(DBManager.offers.c.id == id)
    result = conn.execute(s).fetchone()
    owner = result[1]
    rowID = result[0]
    if UID == owner:
        s = DBManager.offer_data.select().where(DBManager.offer_data.c.id == rowID)
        result = conn.execute(s).fetchone()
        providing = result[2]
        for item in providing:
            q = parseOffer(item)[0]
            print(q)
            i = parseOffer(item)[1]
            print(i)
            x = 0
            while x < int(q):
                s = DBManager.items.update().where(and_(DBManager.items.c.owner == UID, DBManager.items.c.gameId == i)).values(inOffer = False)
                x+=1;

        s = DBManager.offers.delete().where(DBManager.offers.c.id == rowID)
        conn.execute(s)
        s = DBManager.offer_data.delete().where(DBManager.offer_data.c.id == rowID)
        conn.execute(s)

        return "Offer deleted."
    else:
        print("Not correct owner on deletion")

def profileIsPublic(id):
    s = DBManager.users.select().where(DBManager.users.c.id == id)
    result = conn.execute(s).fetchone()
    if result[10] == 1:
        return True
    return False
