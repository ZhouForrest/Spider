import traceback
from scrapy import Request
from scrapy import Selector
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__qyxg_xzxk__credit_tonghua(Spider):

    name = 'Crawler__qyxg_xzxk__credit_tonghua'
    base_url = 'http://thcredit.tonghua.gov.cn'
    start_urls = ['http://thcredit.tonghua.gov.cn/web/dou/permit/non/list']

    def parse(self, response):
        try:
            res = Selector(response)
            totalcount = res.xpath('//div[@class="pagebar"]/@totalcount').extract()
            totalpage = int(int(totalcount[0])/15 + 1)
            for i in range(totalpage):
                url = response.url + '?page.pageNo='+ str(i + 1)
                yield Request(url, callback=self.parse_pages, errback=self.error_back)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning('start_requests error:{}'.format(err_msg))

    def parse_pages(self, response):
        try:
            res = Selector(response)
            url_list = res.xpath('//*[@id="search-result-list"]/li/div/div[2]/a/@href').extract()
            for ul in url_list:
                url = self.base_url + ul
                yield Request(url, callback=self.parse_detail, errback=self.error_back)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning('get max page error:{}'.format(err_msg))

    def parse_detail(self, response):
        try:
            status, item = self.source_item_assembler(response)
            yield item
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning('parse content error:{}'.format(err_msg))

    def error_back(self, response):
        self.logger1.info('err back get page date, url:{}'.format(response.request.url))
