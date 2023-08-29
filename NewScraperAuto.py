import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from concurrent.futures import ThreadPoolExecutor

class Scraper:
    def __init__(self, start_page, end_page):
        self.start_page = start_page
        self.end_page = end_page
        self.data = []

    def parse_page(self, p):
        url = f'https://td-auto.ru/warehouse/?cnt=500&setPageFilter=Y&PAGEN_1={p}'
        print(f"{p} Пройдено страниц")
        r = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(r.text, 'lxml')
        product = soup.find('tbody').findAll('tr')

        for products in product:
            try:
                Code = products.find('td', class_="airus-code").text.strip()
            except: Code = ' '
            try:
                OEM = products.find_all('td')[1].text.strip()
            except: OEM = ' '
            try:
                Name = products.find('td', class_="text-blue name").text.strip()
            except: Name = ' '
            try:
                Items = products.find('td', class_="text-center").text.strip()
            except: Items = ' '
            try:
                Count = products.find('td', class_="text-center text-gray").text.strip()
            except: Count = ' '
            try:
                Price = products.find('span', class_="price").text.strip()
            except: Price = ' '
            self.data.append([Code, OEM, Name, Items, Count, Price])

    def scrape(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.parse_page, range(self.start_page, self.end_page + 1))

    def save_to_csv(self):
        df = pd.DataFrame(self.data, columns=['Code', 'OEM', 'Name', 'Items', 'Count', 'Price'])
        df.to_csv('dataAuto.csv', index=False, encoding='utf-8')

# Use of the class
scraper = Scraper(start_page=1, end_page=65)
scraper.scrape()
scraper.save_to_csv()