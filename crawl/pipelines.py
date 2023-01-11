# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import glob
import os
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    MetaData,
    Integer,
    Text,
    select
)
from scrapy.exceptions import DropItem

class CrawlPipeline:
    def __init__(self):
        _engine = create_engine("sqlite:///data.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _news_items = Table("news", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("date", Text),
                             Column("title", Text),
                             Column("description", Text),
                             Column("detail", Text),
                             Column("logo", Text),
                             Column("img", Text),
                             Column("alt", Text)
                             )
        _metadata.create_all(_engine)
        self.connection = _connection
        self.news_items = _news_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            '''q = select([self.news_items]).where(self.news_items.c.title == item['title'])
            existence = list(self.connection.execute(q))
            if existence:
                raise DropItem("Item existed")
            else:'''
            #print("item: ",item['title'][0])
            '''ins_query = self.news_items.insert().values(
		        date=item['date'][0], title=item['title'][0],
		        description=item['description'][0],
		        detail=item['detail'][0] ,logo=item['logo'][0],
		        img=item['img'][0], alt=item['alt'][0] )
            self.connection.execute(ins_query)'''
            list_of_files = os.listdir("/home/tlukay/crawler/crawl/kinhte_DT")
            number = len(list_of_files)
            filename = './kinhte_DT/KT_DT_'
            filename += str(number+1)
            filename += '.txt'
            if len(item['detail'][0]) != 0:
            	with open(filename, 'a') as f:
            		f.write(item['detail'][0].strip())
            
            
        return item
