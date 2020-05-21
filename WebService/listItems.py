from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String


#Connect to DB (next 2)
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres')
conn = engine.connect()

#Method to list all items in item Table in DB
def listItems(items):
    #searches for item matching itemID inside items table
    s = items.select()
    result = conn.execute(s)
    return result

#Pass in arguments in order: Recipient User ID, Recipient to Provide, Item (ID) to Give
def main(items):
    return listItems(items)

    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
