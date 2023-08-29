import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd

data = []
for p in range(1,65):
    url = f'https://td-auto.ru/warehouse/?cnt=500&setPageFilter=Y&PAGEN_1={p}'

    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')
    product = soup.find('tbody').findAll('tr')



    for products in product:
        try:
            Code = products.find('td', class_="airus-code").text.strip()
        except:
            Code = ' '
        try:
            OEM = products.find_all('td')[1].text.strip()
        except:
            OEM = ' '
        try:
            Name = products.find('td', class_="text-blue name").text.strip()
        except:
            Name = ' '
        try:
            Items = products.find('td', class_="text-center").text.strip()
        except:
            Items = ' '
        try:
            Count = products.find('td', class_="text-center text-gray").text.strip()
        except:
            Count = ' '
        try:
            Price = products.find('span', class_="price").text.strip()
        except:
            Price = ' '
        data.append([Code, OEM, Name, Items, Count, Price])

df = pd.DataFrame(data, columns=['Code', 'OEM', 'Name', 'Items', 'Count', 'Price'])

# Сохранение DataFrame в файл CSV
df.to_csv('data.csv', index=False, encoding='utf-8')