# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from Util.Sql.mongodb import MongoDb


class ZufangPipeline(object):
    def __init__(self):
        # self.client = MongoDb('spider_info', 'zufang')
        self.client = MongoDb('spider_info', 'film')
        self.client.delete_data()
        # self.file_name = open('anjukezufang.csv', 'w')

    def process_item(self, item, spider):
        info = dict(item)
        item_info = json.dumps(info, ensure_ascii=False)
        self.client.insert(json.loads(item_info))
        # self.file_name.write(item_info)
        return item

    def close_spider(self, spider):
        # self.file_name.close()
        self.client.close()
