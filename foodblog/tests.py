from django.test import TestCase



# Create your tests here.
import requests
import random
import csv
import json

url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'


API_KEY = '982cfe3c211cb938'

params = {
    "key": "982cfe3c211cb938",
    "large_area": "SA91",  
    "format": "json",
    "count": 100
}

response = requests.get(url, params=params)
data = response.json()
i = 1

for shop in data['results']['shop']:
    print(shop['name'], shop['address'], end = ' ')
    print(shop['photo']['pc']['l'])



# with open('shops.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = ['name', 'address']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     for shop in data['results']['shop']:
#         writer.writerow({'name': shop['name'], 'address': shop['address']})    


