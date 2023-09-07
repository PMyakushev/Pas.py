import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd
from datetime import datetime
data=[]
for p in range(1,20):
    print(p)
    # url =f'https://ptuning.ru/catalog/farkopy_/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/avtoboksy/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/reylingi_poperechiny/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/korziny/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/zashchita_perednego_bampera/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/zashchita_zadnego_bampera/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/zashchita_porogov/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/reshetki_radiatora/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/komplekty_elektriki/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/komplektuyushchie/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/farkopy_v_razrabotke/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/na_kovrolin/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/v_bagazhnik/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/na_bamper/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/na_dveri_v_proem_dverey/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/bryzgoviki/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/spoylery/?PAGEN_1={p}'
    # url = f'https://ptuning.ru/catalog/kronshteyn_kalitka/?PAGEN_1={p}'
    url = f'https://ptuning.ru/catalog/kolpak_dlya_zapasnogo_kolesa/?PAGEN_1={p}'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    products = soup.findAll('div', class_='element-description-with-counter')
    # print(products)

    for product in products:
        link = product.find('a', class_='element-name intec-cl-text-hover')
        if link is not None:
            data.append('https://ptuning.ru'+ link['href'])

df = pd.DataFrame(data, columns=['Links'])
df.to_csv('Links.csv', mode='a', encoding='utf-8', sep=';', index=False)