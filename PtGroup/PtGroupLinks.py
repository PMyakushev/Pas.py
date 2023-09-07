import requests
from bs4 import BeautifulSoup
import pandas as pd


class Parser:

    def __init__(self, urls):
        self.urls = urls
        self.data = []

    def get_soup(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        return BeautifulSoup(r.text, 'lxml')

    def parse(self):
        for url in self.urls:
            url = url.strip()
            print(f"Processing {url}")

            soup = self.get_soup(url)

            # Характерстики
            characteristics_dict = self.get_characteristics(soup)
            print(characteristics_dict)

            # Ссылка
            hrefs = self.get_links(soup)

            # Описание
            Description = self.get_description(soup)
            print(Description)

            # Наименоваине
            name = self.get_name(soup)
            print(name)

            # Артикул
            sku = self.get_sku(soup)
            print(sku)

            # Прайс
            price = self.get_price(soup)
            print(price)

            self.data.append([name, sku, price, Description, characteristics_dict, hrefs, url])

        df = pd.DataFrame(self.data, columns=['Name', 'SKU', 'Price', 'Description', 'Characteristics', 'hrefs', 'url'])

        # Сохранение файла
        df.to_csv('output.csv', index=False)

    def get_characteristics(self, soup):
        section = soup.find('div', class_='item-characteristics-full')
        if section is None:
            return {}  # Возвращаем пустой словарь если характеристики отсутствуют
        characteristics = section.find_all('div', class_="clearfix characteristic")
        characteristics_dict = {}
        for characteristic in characteristics:
            name = characteristic.find('div', class_="col-xs-6 characteristic-name").text
            value = characteristic.find('div', class_="col-xs-6 characteristic-value").text
            characteristics_dict[name] = value
        return characteristics_dict

    def get_links(self, soup):
        section = soup.find('div', class_='row item-file-list')
        if section is None:
            return []  # Возвращаем пустой список, если документы отсутствуют
        links = section.find_all('a')
        hrefs = ['https://ptuning.ru' + link.get('href') for link in links]  # Добавляем префикс к каждому href
        return hrefs

    def get_description(self, soup):
        description = soup.find('div', class_='item-preview-description')
        if description is None:
            return ''  # возвращаем пустую строку если описание отсутствует
        return description.text.strip()

    def get_name(self, soup):
        name = soup.find('h1', class_='intec-header')
        if name is None:
            return ''  # возвращаем пустую строку если описание отсутствует
        return name.text.strip()

    def get_sku(self, soup):
        sku = soup.find('div', class_='item-article text-muted')
        if sku is None:
            return ''  # возвращаем пустую строку если описание отсутствует
        return sku.text.strip()

    def get_price(self, soup):
        price = soup.find('div', class_='item-current-price')
        if price is None:
            return ''  # возвращаем пустую строку если описание отсутствует
        return price.text.strip()


# Основной код
with open("Links.csv", "r") as f:
    next(f)  # пропустить заголовок
    urls = f.readlines()

p = Parser(urls)
p.parse()