# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from crawlab import save_item

class DuplicatesPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        save_item()
        if adapter["crawl_url"] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {adapter['crawl_url']}")
        else:
            self.urls_seen.add(adapter["crawl_url"])
            if not adapter["corporate_name"] or str(adapter["corporate_name"]) == 'nan':
                raise DropItem(f"Corporate name null at crowl url : {adapter['crawl_url']}")
            # elif not adapter["corporate_url"] or str(adapter["corporate_url"]) == 'nan':
            #     raise DropItem(f"Company url null at crowl url : {adapter['crawl_url']}")
            # elif not adapter["address"] or str(adapter["address"]) == 'nan':
            #     raise DropItem(f"Address null at crowl url : {adapter['crawl_url']}")
            # elif not adapter["tel"] or str(adapter["tel"]) == 'nan':
            #     raise DropItem(f"Tel null at crowl url : {adapter['crawl_url']}")

            else:
                return item