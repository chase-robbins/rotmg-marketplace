from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import urllib
import requests
import os.path
from os import path
import DBManager
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import env


engine = create_engine('postgresql://'+env.db_user+':'+env.db_pass+'@'+env.db_url+':'+env.db_port+'/'+env.db_name)\

conn = engine.connect()

def iterate():
    with open("tradeables.txt", "r") as a_file:
      for line in a_file:
        stripped_line = line.strip()
        start = stripped_line.find("")
        end = stripped_line.find(":")
        id = stripped_line[start:end]
        start = stripped_line.find(":")+1
        name = stripped_line[start:]
        print(name + " " + id)
        s = DBManager.itemIds.insert().values(id = id, Name = name)
        result = conn.execute(s)


def listOffers():
    #searches for item matching itemID inside items table
    s = DBManager.itemIds.select()
    results = conn.execute(s)
    for result in results:
        print(result)
    return results

listOffers()

iterate()
