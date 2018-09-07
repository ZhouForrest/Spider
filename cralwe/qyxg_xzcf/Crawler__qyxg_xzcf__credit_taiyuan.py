# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_taiyuan.py
    Description:    信用太原-行政处罚
    Author:         gyl
    Date:           2018-08-09
    version:        v.1.0
-------------------------------------------------
"""

import re
import traceback
from scrapy.http.request import Request
# from scrapy.http.request.form import FormRequest
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider

class Crawler__qyxg_xzcf__credit_taiyuan(Spider):
    name = "Crawler__qyxg_xzcf__credit_taiyuan"
    start_urls = ["http://www.taiyuan.gov.cn/ztzl/ztzw/xyty/xygs/xzcf/index.shtml", ]

    def parse(self, response):
        try:
            item_list = response.xpath('//*[@id="List"]/tr')
            page_total = int(''.join(re.findall(r'"pageCount": "(\d+)"', response.body.decode())))
            sep = "index"

            # page list
            for page_no in range(2, page_total + 1):
                sep_url = self.start_urls[0].split(sep)
                _url = '{}{}_{}{}'.format(sep_url[0], sep, page_no, sep_url[1])
                self.logger1.info("page list has been saved successfully, url:{}".format(response.url))
                yield Request(_url, callback=self.parse_page, errback=self.err_parse)

            # item list
            for item in item_list:
                details = item.xpath('./td/a/@href').extract()
                detail_url = response.urljoin(details[-1].strip())
                self.logger1.info("page has been saved successfully, url:{}".format(response.url))
                yield Request(detail_url, callback=self.parse_detail, errback=self.err_parse)

        except Exception:
                msg = traceback.format_exc()
                self.logger1.error("parse failed !!! {}".format(msg))

    def parse_page(self, response):
        self.logger1.info("start get detail list in parse_page function, url: {}".format(response.url))
        try:
            item_list = response.xpath('//*[@id="List"]/tr')
            for item in item_list:
                details = item.xpath('./td/a/@href').extract()
                detail_url = response.urljoin(details[-1].strip())
                self.logger1.info("page has been saved successfully, url:{}".format(response.url))
                yield Request(detail_url, callback=self.parse_detail, errback=self.err_parse)
        except Exception:
                msg = traceback.format_exc()
                self.logger1.error("parse_page failed !!! {}".format(msg))

    def parse_detail(self, response):
        try:
            status, item = self.source_item_assembler(response)
            if status:
                yield item
                self.logger1.info("detail has been saved successfully, url:{}".format(response.url))
            else:
                self.logger1.warning("something wrong with detail page, url:{}".format(response.url))
        except Exception:
            msg = traceback.format_exc()
            self.logger1.error("parse_detail failed !!! {}".format(msg))

    def err_parse(self, response):
        self.logger1.error("{} goes wrong...".format(response.request.url))
