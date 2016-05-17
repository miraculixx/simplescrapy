# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field


class TestItem(Item):
    text = Field()


class TestSpider(scrapy.Spider):
    name = "test"
    """
    # this is an actual domain
    allowed_domains = ["api.myjson.com"]
    start_urls = (
        'https://api.myjson.com/bins/1f3ha',
    )
    """
    # tested using a local nginx to be sure 
    # there is not a remote problem
    # server {
    #   listen localhost:5151;
    #    location / {
    #       return 200 '{ "status" : "success" }';
    #   }
    # }

    allowed_domains = ["localhost"]
    start_urls = (
        'http://localhost:5151',
    )

    def parse(self, response):
        item = TestItem()
        item['text'] = response.body
        yield item