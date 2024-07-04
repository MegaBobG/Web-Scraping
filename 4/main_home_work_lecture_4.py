import re

import hashlib
import requests
from lxml import etree


# Получаем контент страницы сайта https://www.lejobadequat.com/emplois
# Функция для получения контента страницы, сохраняет его в файл для повторного использования

def get_content(url):
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print('get from file')
            return content
    except FileNotFoundError:
        response = requests.get(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print('get from server')
        return response.text


# Функция для парсинга HTML с использованием XPath

def parse_html_xpath(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
            tree = etree.HTML(html)
            p = tree.xpath('//h3[@class="jobCard_title"]')
            p = [element.text for element in p]
            print(p)
    except FileNotFoundError:
        print(f"File {filename} not found.")


# Функция для парсинга HTML с использованием регулярных выражений и и измененных заголовков
def parse_html_reg():
    proxy = '116.212.110.18'
    port = 58080

    proxies = {
        'http': f'http://{proxy}:{port}',
        'https': f'http://{proxy}:{port}'
    }

    response = requests.get(
        url='https://www.lejobadequat.com/emplois',
        proxies=proxies,
        timeout=10,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    )
    pattern = '<h3\s+class="jobCard_title">(.+?)<\/h3>'
    job_card = re.findall(pattern, response.text)
    print(job_card)

    with open('job_vacancy.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(job_card))


if __name__ == '__main__':
    # Пример использования функций для получения и парсинга контента

    # url = 'https://www.lejobadequat.com/emplois'
    # html_content = get_content(url)
    #
    # filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(html_content)
    # parse_html_xpath(filename)

    # Вызываем функцию для парсинга с использованием регулярных выражений
    parse_html_reg()
