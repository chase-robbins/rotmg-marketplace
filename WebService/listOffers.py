from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String


#Connect to DB (next 2)
engine = create_engine('postgresql://super:re123123@chaserobbins123-1694.postgres.pythonanywhere-services.com:11694/postgres')

conn = engine.connect()

#Method to list all items in item Table in DB
def listOffers(offers):
    #searches for item matching itemID inside items table
    s = offers.select()
    result = conn.execute(s)
    return result

#Pass in arguments in order: Recipient User ID, Recipient to Provide, Item (ID) to Give
def main(offers):
    return listOffers(offers)

    #Final insertion into transactions ledger
    #insertion = transactions.insert().values(UserID = recepient, MuleID = mule )


if __name__ == '__main__':
    main()
