import requests
from bs4 import BeautifulSoup
import re
import json
import os
from multiprocessing import Pool

def get_product_list():
    all_links = set()
    page = 1

    while True:
        PRODUCT_LIST_URL = f'https://goodereader.com/blog/product-category/e-readers/page/{page}/?orderby=price'
        response = requests.get(PRODUCT_LIST_URL)
        text = response.text

        if 'Not found, error 404' in text:
            break

        html = BeautifulSoup(text, features='lxml')
        links = html.find_all('a')

        for link in links:
            if not 'href' in link.attrs:
                continue
            href = link.attrs['href']

            if not href.startswith('https://goodereader.com/blog/product/'):
                continue
            all_links.add(href)
        page += 1

    return list(all_links)

def get_product_info(url):
    text = requests.get(url).text
    html = BeautifulSoup(text, features='lxml')

    title = html.find('h1', { 'class': 'product_title entry-title'}).text
    price = html.find('span', { 'class': 'woocommerce-Price-amount amount' }).text
    detail = html.find('div', { 'class': 'woocommerce-product-details__short-description'})
    if not detail:
        return
    for element in detail.find_all('p'):
        element.append('\n')
    text = detail.text

    info = {}
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = [part.strip() for part in re.split('：|:|–', line, 1)]
        if len(parts) < 2:
            continue
        info[parts[0]] = parts[1]

    if not len(info):
        return

    info['title'] = title
    info['url'] = url
    info['price'] = price

    return info

def get_all_product_info(force_scrape=False):
    file_name = 'public/products.json'
    if os.path.exists(file_name) and not force_scrape:
        with open(file_name, 'r') as f:
            text = f.read()
            return json.loads(text)

    all_products: List[dict]

    print('Getting product urls')
    product_urls = get_product_list()
    print(f'Found {len(product_urls)} products. Fetching info...')

    with Pool() as p:
        all_products = list(filter(lambda x: x is not None, p.map(get_product_info, product_urls)))

    print('Fetched!')
    json_text = json.dumps(all_products, indent=4)

    with open(file_name, 'w') as f:
        f.write(json_text)

    print('Done!')
    return all_products

if __name__ == '__main__':
    get_all_product_info(force_scrape=True)
