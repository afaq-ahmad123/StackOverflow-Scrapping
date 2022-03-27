# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import itemadapter


class DuplicatePipeline(object):

    def __init__(self):
        return

    def process_item(self, item, spider):
        adapter = itemadapter(item)

        return


class MainPipeline:
    def process_item(self, item, spider):
        return item
