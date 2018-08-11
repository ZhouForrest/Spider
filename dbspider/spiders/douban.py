from scrapy import Selector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from dbspider.items import DbspiderItem


class DouBan(CrawlSpider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']
    # for u in range(10):
    #     url = 'https://movie.douban.com/top250?start=%d' % (u*25)
    #     start_urls.append(url)
    rules = (Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250?.*')),callback="parse_item"), )

    def parse_item(self, response):
        res = Selector(response)
        item = DbspiderItem()

        item['name'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()
        msg = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()').extract()
        item['year'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').re(r'\d+')
        item['director'] = msg[0].strip().replace('\xa0', '')
        item['avatar'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()
        return item



