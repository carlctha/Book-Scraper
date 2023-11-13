import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["campusbokhandeln.se"]
    start_urls = ["https://campusbokhandeln.se/kurser/linkopings-universitet/data-it"]

    def parse(self, response):
        pass
