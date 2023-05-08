import scrapy
from scrapy.selector import Selector


class CharacterSpiderSpider(scrapy.Spider):
    name = "character_spider"
    start_urls = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]

    def parse(self, response):
        tables = response.xpath('//table[@class="wikitable sortable"]')
        for table in tables:
            rows = table.xpath(".//tr")
            for row in rows:
                tds = row.xpath(".//a")
                if tds:
                    if "Character" not in tds.attrib["href"]:
                        next_page_url = (
                            "https://onepiece.fandom.com/" + tds.attrib["href"]
                        )
                        yield response.follow(
                            next_page_url, callback=self.character_parse
                        )

    def character_parse(self, response):
        # print("hey")
        # print(response.xpath('//div[@class="pi-data-value"]').get())

        name_div = response.xpath(
            "//div[@class='pi-item pi-data pi-item-spacing pi-border-color']/div[@class='pi-data-value pi-font']"
        )[2].get()
        selector = Selector(text=name_div)
        yield {
            "character": selector.xpath(
                '//div[@class="pi-data-value pi-font"]/text()'
            ).get()
        }
