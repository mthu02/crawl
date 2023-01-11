import scrapy
from scrapy.crawler import CrawlerProcess
import glob
import os
from itemloaders.processors import MapCompose, Join
from scrapy import Request
from urllib import parse
from scrapy.loader import ItemLoader
from crawl.items import CrawlItem

class KinhteSpider(scrapy.Spider):
    name = 'kinhte'
    allowed_domains = ['dantri.com.vn']
    start_urls = ['https://dantri.com.vn/xa-hoi.htm',
	]

    total_scraped = 0
    def parse(self, response):
        next_selectors = response.xpath('//*[contains(@class, "btn-page next-page")]//@href')
        for url in next_selectors.extract(): 
            yield Request(parse.urljoin(response.url, url), 
                          callback=self.parse, 
                          dont_filter=True) 
 
        item_selectors = response.xpath('//*[contains(@class, "item-news item-news-common thumb-left")]//div//a//@href') 
        #item_not_selectors = response.xpath('//*[contains(@class, "item-news item-news-common thumb-left")]//div//div//p//a//@href')
        #print("item: ",item_not_selectors)
        for url in item_selectors.extract():
            if self.total_scraped == 5: break
            else:
            	yield Request(parse.urljoin(response.url, url), 
                          callback=self.getItem, 
                          dont_filter=True)
 
    def getItem(self, response): 
        ld = ItemLoader(item=CrawlItem(), response=response) 
        ld.add_xpath('title', '//*[contains(@class, "title-detail")]//text()')
        ld.add_xpath('date', '//*[contains(@class, "date")]//text()')
        ld.add_xpath('description', '//*[contains(@class, "description")]//text()', Join())
        ld.add_xpath('detail', '//*[contains(@class, "Normal")]//text()', Join())
        ld.add_xpath('logo', '//*[contains(@class, "logo")]//@src')
        ld.add_xpath('img', '//*[contains(@class, "fig-picture")]//@data-src', Join())
        ld.add_xpath('alt', '//*[contains(@class, "fig-picture")]//@alt', Join())
        
        self.total_scraped = self.total_scraped + 1
        #print('Total scrapes:', self.total_scraped)
        yield ld.load_item()

#process = CrawlerProcess()
#process.crawl(KinhteSpider)
#process.start(stop_after_crawl=False)
