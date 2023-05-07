import scrapy


class CharacterSpiderSpider(scrapy.Spider):
    name = "character_spider"
    allowed_domains = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]
    start_urls = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]

    def parse(self, response):
        tables = response.xpath('//table[@class="wikitable sortable"]')
        for table in tables:
            rows = table.xpath(".//tr")
            for row in rows:
                tds = row.xpath(".//a")
                next_page_url = "https://onepiece.fandom.com/" + tds.attrib["href"]
                print(next_page_url)
                if "character" not in next_page_url:
                    yield response.follow(next_page_url, callback=self.character_parse)

    def character_parse(self, response):
        print(response.css("aside").get())
