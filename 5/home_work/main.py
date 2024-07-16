import re
import hashlib
import requests

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


def parse_html_reg():
    proxy = '67.43.227.226'
    port = 18123

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

    job_cards = []

    titles = re.findall(title_pattern, response.text)
    urls = re.findall(url_pattern, response.text)

    for title, url in zip(titles, urls):
        job_cards.append({'title': title, 'url': url})

    return job_cards


def write_json(job_cards):
    if job_cards:
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(job_cards, f, ensure_ascii=False, indent=4)
        print("Data saved to jobs.json")
    else:
        print("No data to save.")


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
        """, (job['title'], job['url']))

    conn.commit()
    conn.close()
    print("Data saved to jobs.db")


# Пример использования:
if __name__ == "__main__":
    jobs_data = parse_html_reg()
    write_json(jobs_data)
    write_sqlite(jobs_data)
