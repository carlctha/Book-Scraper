import scrapy, smtplib
from scrapy.crawler import CrawlerProcess
from email.message import EmailMessage
from decouple import config


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["campusbokhandeln.se"]
    start_urls = [
        "https://campusbokhandeln.se/kurser/linkopings-universitet/data-it",
        "https://campusbokhandeln.se/kurser/linkopings-universitet/matematik-statistik"
    ]

    custom_settings = {
        "FEEDS": {
            "books.csv": {
                "format": "csv"
            }
        }
    }

    def parse(self, response):
        books = response.css("table#gridtable tbody tr")
        my_courses = [
            "725G90", "TSEA28", "TDDD86", "TDDD37",
            "TATA24", "92MA14", "TATA83", "TNIU66",
        ]
        
        for book in books:
            course_code = book.css("a::text").extract()[1]
            book_page_url = "https://campusbokhandeln.se" + book.css("a").attrib["href"]
            if course_code in my_courses:
                yield response.follow(book_page_url, callback=self.parse_page)

    def parse_page(self, response):
        book_list = response.css("div#books div.product-module")
        book_name = response.css("div#books p.title a::text")
        book_price = response.css("div#books p.price span::text")

        if len(book_list) > 1:
            for i in range(len(book_list)):
                yield {
                    "name": book_name.extract()[i],
                    "price": book_price.extract()[i]
                }
        else:
            yield {
                "name": book_name.extract_first(),
                "price": book_price.extract_first()
            }


def send_mail():
    EMAIL_USER = config("EMAIL_USER")
    EMAIL_PASS = config("EMAIL_PASS")

    with open("books.csv", "r") as file:
        data = file.read()

    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_USER
    message["subject"] = "Kursböcker"
    message.set_content("message body")
    message.add_attachment(data, filename="books.csv")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(message)
    server.quit()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BookspiderSpider)
    process.start()

    send_mail()
