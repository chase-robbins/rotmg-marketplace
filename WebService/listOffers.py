from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
import env


#Connect to DB (next 2)
engine = create_engine('postgresql://'+env.db_user+':'+env.db_pass+'@'+env.db_url+':'+env.db_port+'/'+env.db_name)\

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
