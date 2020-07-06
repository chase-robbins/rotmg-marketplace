from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String


#Connect to DB (next 2)
engine = create_engine('postgresql://postgres:testingPassword@localhost:5432/postgres')

conn = engine.connect()

#Method to find the mule that is holding item in question
def findMule(ownerID, itemID, items):
    #searches for item matching itemID inside items table
    s = items.select().where(items.c.id == itemID)
    result = conn.execute(s)
    row = result.fetchone()
    nameOfItem = row[1]
    muleID = row[2]
    print("Mule located. Item " + nameOfItem + " is located on mule with ID " + str(muleID) )
    return muleID

#Pass in arguments in order: Recipient User ID, Recipient to Provide, Item (ID) to Give
def main(recipient, providing, toGive, items):
    print("Recipiet " + recipient + " will recieve " + str(toGive) + " via mule " + str(findMule(3, toGive, items)) + " in exchange for " + providing)
    findMule(3, toGive, items)

    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
