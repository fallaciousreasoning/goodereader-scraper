import requests
from bs4 import BeautifulSoup
import re
import json
import os

def get_product_list():
    all_links = set()
    page = 1

    while True:
        PRODUCT_LIST_URL = f'https://goodereader.com/blog/product-category/e-readers/page/{page}/?orderby=price'
        response = requests.get(PRODUCT_LIST_URL)
        text = response.text

        if 'Not found, error 404' in text:
            break

        html = BeautifulSoup(text)
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
    html = BeautifulSoup(text)

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
            
        parts = [part.strip() for part in re.split('：|:', line, 1)]
        if len(parts) < 2:
            continue
        info[parts[0]] = parts[1]

    if not len(info):
        return

    info['title'] = title
    info['url'] = url
    info['price'] = price

    return info

def get_all_product_info():
    file_name = 'cache/products.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            text = f.read()
            return json.loads(text)

    all_products = []
    product_urls = get_product_list()
    print(f'Found {len(product_urls)} products')
    for product in product_urls:
        info = get_product_info(product)
        if not info:
            continue

        all_products.append(info)

    json_text = json.dumps(all_products, indent=4)

    if not os.path.exists('cache'):
        os.makedirs('cache')

    with open(file_name, 'w') as f:
        f.write(json_text)

    return all_products
