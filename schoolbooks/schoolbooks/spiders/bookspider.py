import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["campusbokhandeln.se"]
    start_urls = ["https://campusbokhandeln.se/kurser/linkopings-universitet/data-it"]

    def parse(self, response):
        books = response.css("table#gridtable tbody tr")
        for book in books:
            book_name = book.css("a.tw-break-all::text").extract()
            book_page_link = "https://campusbokhandeln.se/kurser/linkopings-universitet/data-it" + book.css("a").attrib["href"]
            yield {
                "name": book_name[0],
                "link": book_page_link
            }
