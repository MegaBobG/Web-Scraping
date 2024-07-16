import scrapy

class QuoteHomeWorkSpider(scrapy.Spider):
    name = "quote_home_work"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    max_pages = 1  # Максимальное количество страниц для скрапинга (включая первую)

    custom_settings = {
        'DOWNLOAD_DELAY': 1  # Задержка между запросами для предотвращения перегрузки сервера
    }

    def parse(self, response):
        token = response.xpath('//input[@name="csrf_token"]/@value').get()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # Проверяем успешность авторизации
        if "Logout" in response.text:
            self.logger.info("Вход выполнен успешно")

            # Начинаем парсинг с первой страницы
            yield response.follow(url="/page/1/", callback=self.parse_quotes)
        else:
            self.logger.error("Ошибка входа")

    def parse_quotes(self, response):
        # Пример парсинга цитат со страницы после авторизации
        quotes = response.xpath('//div[@class="quote"]')

        for quote in quotes:
            text = quote.xpath('.//span[@class="text"]/text()').get()
            author = quote.xpath('.//span/small[@class="author"]/text()').get()

            yield {
                'quote': text.strip() if text else None,
                'author': author.strip() if author else None
            }

        # Проверяем, есть ли кнопка "next" и продолжаем парсинг если есть
        next_btn = response.xpath('//li[@class="next"]/a/@href').get()
        if next_btn and self.max_pages >= 1:
            self.max_pages -= 1
            next_page = response.urljoin(next_btn)
            yield response.follow(next_page, callback=self.parse_quotes)
