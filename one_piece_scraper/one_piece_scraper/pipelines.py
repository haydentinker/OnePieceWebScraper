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
        # if len(adapter.keys()) < 6:
        #     raise DropItem("missing value")
        for i in adapter.keys():
            if adapter[i] == None:
                raise DropItem("Missing values")
            if adapter[i] == '"':
                raise DropItem("Missing values")
            adapter[i] = adapter[i].strip(";")
            adapter[i] = adapter[i].strip('"')
            adapter[i] = adapter[i].strip("'")
            adapter[i] = adapter[i].strip()
            adapter[i] = re.sub("\(.*?\)", "", adapter[i])
            adapter[i] = re.sub("\[.*?\]", "", adapter[i])
        # Check for dupl
        # url, character, anime_debut, affiliations, occupations, birthday
        # Clean Name
        return item
