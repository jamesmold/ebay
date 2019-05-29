#The eBay API date range is limited to 3 months back and 100 records only

key = 'insert your key here -- sign-up at eBay.com for an API key'

import json
import requests
import pandas as pd

df = pd.DataFrame(columns = ['Title', 'Price', 'Condition', 'ID', 'URL', 'End Date'])

search_term = input("Enter search term: ")

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
    condition = item['condition'][0]['conditionDisplayName'][0]
    price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
    itemurl = item['viewItemURL'][0]
    itemid = item['itemId'][0]
    end = item['listingInfo'][0]['endTime'][0]
    sales = item['sellingStatus'][0]['sellingState'][0]
    if sales == "EndedWithSales":
        df = df.append({'Title':title, 'Price':price, 'Condition':condition, 'ID':itemid, 'URL':itemurl, 'End Date':end}, ignore_index=True)
        
print(df)
df.to_excel('ebay.xlsx')