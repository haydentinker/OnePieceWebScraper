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
        url = response.xpath("//figure[@class='pi-item pi-image']/a/@href").get()

        name = response.xpath('//div[@data-source="ename"]/div//text()').get()

        anime_debut = response.xpath('//div[@data-source="first"]/div//text()').get()
        affiliations = response.xpath(
            '//div[@data-source="affiliation"]/div//text()'
        ).get()
        occupations = response.xpath(
            '//div[@data-source="occupation"]/div//text()'
        ).get()
        birthday = response.xpath('//div[@data-source="birth"]/div//text()').get()
        yield {
            "url": url,
            "name": name,
            "anime_debut": anime_debut,
            "affiliations": affiliations,
            "occupations": occupations,
            "birthday": birthday,
        }
