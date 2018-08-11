import scrapy
from scrapy import Selector


class QiDianSpider(scrapy.spiders.Spider):
    name = 'qidian'
    start_urls = ["https://www.qidian.com/",]

    def parse(self, response):
        current_url = response.url
        print(current_url)
        body = response.body
        print(body)
        unicode_body = response.body_as_unicode()
        print(unicode_body)
        res = Selector(response)
        xiaoshuo_type = res.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        xiaoshuo_href = res.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(xiaoshuo_type, xiaoshuo_href)


