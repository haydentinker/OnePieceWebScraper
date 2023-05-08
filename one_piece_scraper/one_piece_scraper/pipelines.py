# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class OnePieceScraperPipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Check Length of Item
        if len(adapter.keys()) != 6:
            raise DropItem(("Missing fields"))
        # Check for duplicates
        if adapter["character"] in self.names_seen:
            raise DropItem("Duplicate character")
        # url, character, anime_debut, affiliations, occupations, birthday
        # Clean Name
        name = adapter.get("character")
        name = re.sub("\(.*?\)", "", name)
        adapter["character"] = re.sub("\[.*?\]", "", name)
        return item
