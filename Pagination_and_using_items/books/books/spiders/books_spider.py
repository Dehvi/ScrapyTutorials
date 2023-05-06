import scrapy
from books.items import BooksItem

class BooksSpiderSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):

        books = response.css("article.product_pod")
        # loop all books and goto the book page to scrape the data
        for book in books:
            full_url =  response.urljoin(book.css("h3 a").attrib['href'])
            yield scrapy.Request(full_url, callback=self.parse_book)
        # after all books on page are searched. Get the next page link
        next_page_url = response.css("li.next a").attrib['href']
        
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)
        
    def parse_book(self, response):
        """ Parses the book data and saves into an item which is then yielded"""
        item = BooksItem()
        product_main = response.css("div.col-sm-6.product_main")
        item['title'] = product_main.css("h1::text").get()
        item['price'] = product_main.css("p.price_color::text").get()

        product_info = response.css("table.table.table-striped")     # Contains the html table with product information
        item['upc'] = product_info.css("td::text").get()
        item['product_type'] = product_info.css("td::text")[1].get()
        parse_numbers = "".join(x for x in product_info.css("td::text")[5].get() if x.isdigit())
        item['in_stock'] = int(parse_numbers) 
        yield item
        
        