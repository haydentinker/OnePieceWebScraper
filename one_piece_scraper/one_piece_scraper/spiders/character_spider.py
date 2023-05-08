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
        url_div = response.xpath("//figure[@class='pi-item pi-image']/a/@href").get()

        name_div = response.xpath(
            "//div[@class='pi-item pi-data pi-item-spacing pi-border-color']/div[@class='pi-data-value pi-font']"
        )[2].get()
        name_selector = Selector(text=name_div)
        anime_debut = response.xpath(
            "//div[@class='pi-item pi-data pi-item-spacing pi-border-color']/div[@class='pi-data-value pi-font']"
        )[3].get()
        anime_selector = Selector(text=anime_debut)
        affiliations = response.xpath(
            "//div[@class='pi-item pi-data pi-item-spacing pi-border-color']/div[@class='pi-data-value pi-font']"
        )[4].get()
        affiliations_selector = Selector(text=affiliations)
        occupations = response.xpath(
            "//div[@class='pi-item pi-data pi-item-spacing pi-border-color']/div[@class='pi-data-value pi-font']"
        )[5].get()
        occupations_selector = Selector(text=occupations)
        birthday = response.xpath('//div[@data-source="birth"]')
        birth_elements = response.xpath('//div[@data-source="birth"]')
        yield {
            "url": url_div,
            "character": name_selector.xpath(
                '//div[@class="pi-data-value pi-font"]/text()'
            ).get(),
            "anime_debut": anime_selector.xpath("//a/text()")[1].get(),
            "affiliations": affiliations_selector.xpath("//@title").get(),
            "occupations": occupations_selector.xpath("//@title").get(),
            "birthday": birth_elements.get(),
        }
