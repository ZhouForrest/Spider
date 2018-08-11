import json

from scrapy import Request
# from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

from lianjiaspider.items import LianjiaspiderItem


class LianJiaSpider(RedisSpider):
    name = 'lianjia'
    # base_url = 'https://cd.lianjia.com/ershoufang/pg{num}/'
    start_urls = ['https://cd.lianjia.com/ershoufang/', ]
    area_url = 'https://cd.lianjia.com/'
    # redis_key = 'lianjia:start_urls'

    def parse(self, response):
        results = Selector(response)
        href = results.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a/@href').extract()
        area_name = results.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a/text()').extract()
        for a in range(len(href)):
            yield Request(self.area_url + href[a], callback=self.parse_house, meta={'name': area_name[a], 'url': self.area_url + href[a]})

    # def start_requests(self):
    #     for num in range(1, 101):
    #         yield Request(self.base_url.format(num=num))
    #
    def parse_house(self, response):
        res = Selector(response)
        results = res.xpath('/html/body/div[4]/div[1]/ul//li[@class="clear"]')
        area = response.meta.get('name')
        url = response.meta.get('url')
        item = LianjiaspiderItem()
        for result in results:
            item['code'] = result.xpath('./div[1]//div[@class="title"]/a/@data-housecode').extract().pop()
            item['title'] = result.xpath('./div[1]//div[@class="title"]/a/text()').extract().pop()
            item['loupan'] = result.xpath('./div[1]//div[@class="houseInfo"]/a/text()').extract().pop()
            item['houseInfo'] = result.xpath('./div[1]//div[@class="houseInfo"]/text()').extract()
            item['flood'] = result.xpath('./div[1]//div[@class="flood"]/div/text()').extract().pop()
            item['tag'] = result.xpath('./div[1]//div[@class="tag"]/span/text()').extract()
            item['img'] = result.xpath('./a/img/@data-original').extract().pop()
            item['total'] = result.xpath('./div[1]//div[@class="priceInfo"]/div/span/text()').extract()[0] + '万'
            item['price'] = result.xpath('./div[1]//div[@class="priceInfo"]/div/span/text()').extract()[1]
            item['area'] = area
            yield item

        total = res.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/@page-data').extract()
        pages = json.loads(total[0])['totalPage']
        for page in range(2, pages+1):
            yield Request(url+'pg'+str(page), callback=self.parse_house, meta={'name': area,'url': url})


