import os
import re
import hashlib
import json
from time import time
from typing import List

from bs4 import BeautifulSoup
import requests
from multiprocessing.pool import Pool


def get_content(url):
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text


def parse_html():
    url = 'https://www.bbc.com/sport'
    content = get_content(url)

    soup = BeautifulSoup(content, 'lxml')

    data = []

    blocks = soup.find_all('div', {'type': ['article', 'topic']})
    for block in blocks:
        href = block.find('a').get('href').strip()
        full_url = 'https://www.bbc.com/' + href
        data.append({"Link": full_url})

    with open('data_BBC.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(data)
    print(len(data))


def parse_page(page_url):
    content = get_content(page_url)

    soup = BeautifulSoup(content, 'lxml')

    # data = []

    blocks = soup.find('div', {'data-component': 'topic-list'})
    if blocks:
        list_items = blocks.find_all('li')
        for li in list_items:
            link = li.find('a')
            if link:
                href = link.get('href')
                links = link.text.strip()
                # data.append({'Link': text})
    # print(data)

    return {'url': page_url, 'site': links}


def parse_sync():
    url = 'https://www.bbc.com/sport'
    content = get_content(url)

    soup = BeautifulSoup(content, 'lxml')

    data = []

    blocks = soup.find_all('div', {'type': ['article', 'topic']})
    for block in blocks:
        href = block.find('a').get('href').strip()
        full_url = 'https://www.bbc.com/' + href
        page_data = parse_page(url)
        data.append(page_data)

    with open('sync.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # parse_html()
    parse_page('https://www.bbc.com/sport/football/articles/c134enzzg26o')
