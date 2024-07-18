import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Функция парсинга с помощью Selenium
def parse_selenium():
    site = 'https://jobs.marksandspencer.com/job-search'
    driver = webdriver.Chrome()

    max_pages = 2
    result = []

    # Цикл по страницам для парсинга
    for page in range(1, max_pages + 1):
        driver.get(site)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[aria-label="Page {page}"]')))
        page_link = driver.find_element(By.CSS_SELECTOR, f'a[aria-label="Page {page}"]').get_attribute('href')
        driver.get(page_link)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-Hits-item')))

        # Получение списка элементов с вакансиями на текущей странице
        jobs = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
        for job in jobs:
            title = job.find_element(By.CSS_SELECTOR, 'h3').text
            link = job.find_element(By.CSS_SELECTOR, 'a[class*="c-btn--primary"]').get_attribute('href')

            result.append({
                'title': title,
                'url': link
            })

    driver.quit()

    with open('jobs_selenium_home_work.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parse_selenium()
