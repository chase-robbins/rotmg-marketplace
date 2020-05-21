from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import DBManager
import InitiateTransaction
import listItems
import createAccount
import pwSalting

def listThem():
    return listItems.main(DBManager.items)

def createAcc(ign, email, password):
    createAccount.main(ign, email, pwSalting.hash_password(password), DBManager.users)
