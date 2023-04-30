import scrapy


class BooksSpiderSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            yield {
                'book_name': book.css("h3 a::attr(title)").get(),
                'price': book.css("div.product_price p.price_color::text").get(),
                'link': book.css("h3 a").attrib['href']
            }
        
