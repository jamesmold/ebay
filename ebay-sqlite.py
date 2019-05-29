#The eBay API date range is limited to 3 months back and 100 records only

key = 'insert your key here -- sign-up at eBay.com for an API key'

import json
import requests
import sqlite3

search_term = input("Enter search term: ")
dbname = input("Enter dB name: ")

conn = sqlite3.connect(dbname + ".sqlite")
cur = conn.cursor()

url = ('http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=findCompletedItems\
&sortOrder=PricePlusShippingHighest\
&SERVICE-VERSION=1.13.0\
&SECURITY-APPNAME=' + key +
'&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&itemFilter(0).name=Condition\
&itemFilter(0).value=Used\
&itemFilter(1).name=MaxPrice\
&itemFilter(1).value=50000.0\
&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=USD\
&itemFilter(2).name=MinPrice\
&itemFilter(2).value=0.0\
&itemFilter(2).paramName=Currency\
&itemFilter(2).paramValue=USD\
&keywords=' + search_term)

apiResult = requests.get(url)
parseddoc = apiResult.json()

for item in (parseddoc["findCompletedItemsResponse"][0]["searchResult"][0]["item"]):

    title = item["title"][0]
    price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
    itemurl = item['viewItemURL'][0]
    sales = item['sellingStatus'][0]['sellingState'][0]
    itemid = item['itemId'][0]
    end = item['listingInfo'][0]['endTime'][0]

    if sales == "EndedWithSales": #inserts only SOLD items -- change to EndedWithoutSales or remove completely if want to see all ended listings
        try: #try and except used as the dB will return an error if an insert of record with the same ID is attempted
            cur.execute('''CREATE TABLE IF NOT EXISTS sales
            (Title TEXT, Price TEXT NUMERIC, URL TEXT, ID INTEGER UNIQUE, End TEXT)''')
            cur.execute('INSERT INTO sales (Title, Price, URL, ID, End) VALUES (?, ?, ?, ?, ?)',
            (title, price, itemurl, itemid, end))
        except:
            pass

conn.commit()
cur.close()