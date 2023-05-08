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
                if tds:
                    if "Character" not in tds.attrib["href"]:
                        next_page_url = (
                            "https://onepiece.fandom.com/" + tds.attrib["href"]
                        )
                        yield response.follow(
                            next_page_url, callback=self.character_parse
                        )

    def character_parse(self, response):
        print(
            response.xpath(
                '//aside[@role="region"]and contains(@class, "portable-infobox")'
            )
        )
        yield {
            "character": response.xpath(
                '//aside[@role="region"]and contains(@class, "portable-infobox")'
            )
        }
