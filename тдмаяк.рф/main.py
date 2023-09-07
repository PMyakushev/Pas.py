import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# All your previous code ...

def fetch_url(p):
    print(p)
    # url = f"https://тдмаяк.рф/avtotovary/?page={p}"
    # url = f"https://тдмаяк.рф/avtosvet/?page={p}"
    # url = f"https://тдмаяк.рф/bytovye-i-turisticheskie-tovary/?page={p}"
    # url = f"https://тдмаяк.рф/instrument/?page={p}"
    # url = f"https://тдмаяк.рф/elektrotehnika/?page={p}"
    # url = f"https://тдмаяк.рф/novye-forsazh/?page={p}"
    url = f"https://тдмаяк.рф/knov/?page={p}"


    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')

    # Your classes and regex here ...
    product_classes = ['flexdiscount-product-wrap salesku_plugin-product view_class thumbs_v2 col-md-3 col-sm-6',
                       'flexdiscount-product-wrap salesku_plugin-product view_class col-md-3 col-sm-6 col-xs-12','flexdiscount-product-wrap salesku_plugin-product view_class']

    regex = re.compile('|'.join(product_classes))


    product = soup.findAll('li', class_=regex)

    # Если список продуктов пуст, возвращаем None
    if not product:
        print("Нет данных на странице.")
        return None

    # Иначе, возвращаем полученные данные
    data = []
    for products in product:
        name = products.find('div', class_="product_title").text
        price = products.find('div', class_="pricing align-center").text
        sku = products.find('div', class_="sku_heading").text
        data.append([name, price, sku])

    return data

# Используем ThreadPoolExecutor для многопоточного исполнения
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_url, range(1, 200))

# Собираем данные в один список
data = []
for result in results:
    if result is not None:
        data.extend(result)
header = ['name', 'price', 'sku']
df = pd.DataFrame(data, columns=header)

# Сохраняем DataFrame в файл CSV
df.to_csv('file_name.csv', sep=';', encoding = "utf8")
# Saving data to CSV as before...