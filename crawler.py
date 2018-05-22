__author__ = "anhvd"

# crawling all items from SLP 2018 Fall Winter 18 - Preorder collection

import requests
from bs4 import BeautifulSoup
import html
import re
import sys

BASE_URL = r'https://www.ysl.com/us/'
api = r'https://www.ysl.com/Search/RenderProductsAsync?ytosQuery=true&department=mfall18_gallery&gender=U&season=A%2CP%2CE&yurirulename=searchwithdepartment&page=1&productsPerPage={}&suggestion=false&facetsvalue=&totalPages=12&totalItems=248&partialLoadedItems=22&itemsToLoadOnNextPage=22&siteCode=SAINTLAURENT_US'

PRODUCTS_PER_PAGE = 999

def save_html(soup):
    with open('save.html', 'w', encoding='utf-8' ) as file:
        file.write(str(soup))

def get_cookie():
    content = str()
    with open('cookie.txt', 'r') as file:
        for line in file:
            content += line
    return content

def get_product_urls(file_name = None):
    if file_name is not None:
        urls = list()
        with open(file_name, 'r') as file:
            for line in file:
                urls.append(line.rstrip('\n'))
    else:
        headers = {
            'cookie': get_cookie() 
        }
        url = api.format(PRODUCTS_PER_PAGE)
        print(url)
        # r = requests.get(url, headers=headers)
        s = requests.Session()
        s.get(BASE_URL)
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        save_html(soup)
        urls = list(map(lambda url: url['href'], soup.find_all('a')))
    return urls

def get_product(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    product ={
        'name': '',
        'description': '',
        'details': '',
        'imgs': {},
    }
    product['name'] = soup.select_one('span.modelName.inner').text.strip()
    description_content = soup.select('div.descriptionContent.accordion-content')
    product['description'] = description_content[0].text.strip()
    product['details'] = description_content[1].text.strip()
    # save_html(str(soup))
    imgs = list(map(lambda li: li.find('img'),soup.find('ul', {'class':'alternativeImages'}).find_all('li')))
    print(product)
    for index, img in enumerate(imgs, start=1):
        print('{} - data-origin: {}\ndata-srcset: {}'.format(index,img.get('data-origin'), html.unescape(img['data-srcset']).split(',')[-1]))
        # print(str(img))

def main():
    product_urls = list()
    if len(sys.argv) > 1:
        product_urls = get_product_urls(sys.argv[1])
    else:
        product_urls = get_product_urls()
    with open('urls.txt', 'w', encoding='utf-8') as file:
        for url in product_urls:
            file.write('{}\n'.format(url))
    print('Total items: {}'.format(len(product_urls)))
    for url in product_urls[:5]:
        print(url)
        get_product(url)

if __name__ == '__main__':
    main()