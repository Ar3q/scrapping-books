import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com/'
    ]

    def parse(self, response):
        books_hrefs = response.css(
            'article.product_pod h3 > a::attr(href)').getall()

        next_page = response.css('li.next > a::attr(href)').get()

        for href in books_hrefs:
            yield response.follow(href, self.parse_book)

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        title = response.css('article.product_page h1::text').get()
        description = response.css('div#product_description + p::text').get()

        yield {
            'product_description': description,
            'title': title,
        }
