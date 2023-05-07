import scrapy


class CharacterSpiderSpider(scrapy.Spider):
    name = "character_spider"
    allowed_domains = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]
    start_urls = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]

    def parse(self, response):
        table_rows = response.css("table tr")
        for row in table_rows:
            print(table_rows.css("td a ::attr(href)").get())
