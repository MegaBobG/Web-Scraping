import re
import hashlib
import requests
from lxml import etree
import json
import sqlite3


# Функция для получения контента страницы с возможностью кэширования
def get_content(url):
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            print('get from file')
            return f.read()
    except FileNotFoundError:
        response = requests.get(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print('get from server')
        return response.text


# Функция для парсинга HTML с использованием XPath
# def parse_html_xpath(html_content):
#     tree = etree.HTML(html_content)
#     job_cards = []
#     base_url = 'https://www.lejobadequat.com'
#     for element in tree.xpath('//h3[@class="jobCard_title"]'):
#         title = element.text.strip()
#         relative_url = element.xpath('./parent::a/@href')[0]
#         full_url = base_url + relative_url
#         job_cards.append([title, full_url])
#     print(job_cards)
#     return job_cards


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


    # Паттерн для извлечения заголовков вакансий
    title_pattern = r'<h3\s+class="jobCard_title">(.+?)<\/h3>'

    # Паттерн для извлечения URL из ссылки на вакансию
    url_pattern = r'<a\s+[^>]*href="([^"]+)"[^>]*class="jobCard_link"'
    urls = re.search(url_pattern, response.text).group(1)

    job_cards = []

    titles = re.findall(title_pattern, response.text)
    for title in titles:
        for url in urls:
            job_cards.append([title, url])

    return job_cards



# Функция для записи данных в JSON файл
def write_json(job_cards):
    if job_cards:
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(job_cards, f, ensure_ascii=False, indent=4)
        print("Data saved to jobs.json")
    else:
        print("No data to save.")


# Функция для записи данных в базу данных SQLite
def write_sqlite(job_cards):
    filename = 'jobs.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Создание таблицы, если она не существует
    sql = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT
        )
    """
    cursor.execute(sql)

    # Вставка данных в таблицу
    for job in job_cards:
        cursor.execute("""
            INSERT INTO jobs (title, url)
            VALUES (?, ?)
        """, (job[0], job[1]))

    conn.commit()
    conn.close()
    print("Data saved to jobs.db")


if __name__ == '__main__':
    page_url = 'https://www.lejobadequat.com/emplois'
    page_html_content = get_content(page_url)
    jobs = parse_html_xpath(page_html_content)
    write_json(jobs)
    write_sqlite(jobs)
