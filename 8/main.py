import json
from time import time
from urllib.parse import urljoin

import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def parse_selenium():
    site = 'https://jobs.aon.com'
    driver = webdriver.Chrome()

    max_pages = 11
    result = []

    for page in range(1, max_pages):
        driver.get(urljoin(site, f'jobs?page={page}'))
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'job-title-link')))

        # 1. use BeautifulSoup
        # content = driver.page_source
        # soup = BeautifulSoup(content, 'lxml')
        # jobs = soup.find_all(class_='job-title-link')
        # for job in jobs:
        #     link = urljoin(site, job.get('href'))
        #     title = job.find('span').text
        #     result.append({
        #         'link': link,
        #         'title': title
        #     })

        # 2. use Selenium
        jobs = driver.find_elements(By.CLASS_NAME, 'job-title-link')
        for job in jobs:
            link = job.get_attribute('href')
            title = job.find_element(By.TAG_NAME, 'span').text
            result.append({
                'link': link,
                'title': title
            })

    driver.quit()

    with open('jobs_selenium.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


def parse_form():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get('https://jobs.aon.com/jobs?page=1')

    driver.implicitly_wait(3) # not good way to wait
    wait.until(EC.presence_of_element_located((By.ID, 'search-results-indicator')))  # best way to wait

    before = driver.find_element(By.ID, 'search-results-indicator').text
    print('Count before:', before)

    title_input = driver.find_element(By.ID, 'keyword-search')
    title_input.send_keys('Engineer')

    driver.implicitly_wait(1)

    button = driver.find_element(By.ID, 'search-btn')
    # button.submit()
    button.click()

    driver.implicitly_wait(3)

    after = driver.find_element(By.ID, 'search-results-indicator').text
    print('Count after:', after)

    driver.quit()


def parse_site():
    max_page = 11
    result = []
    for page in range(1, max_page):
        print(f'Page: {page} ...')
        response = requests.get(
            url=f'https://jobs.aon.com/api/jobs?page={page}&keywords=Engineer&sortBy=relevance&internal=false&deviceId=undefined&domain=aon.jibeapply.com',
            headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }
        )
        data = response.json()['jobs']
        for job in data:
            link = 'https://jobs.aon.com/jobs/' + str(job['data']['slug'])
            title = job['data']['title']

            result.append({
                'link': link,
                'title': title
            })

    with open('jobs_requests.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # parse_selenium()
    # parse_form()

    t = time()
    parse_site()
    print(time() - t) # 12.431

    # t = time()
    # parse_selenium()
    # print(time() - t)  # 47.055
