# -*- coding: utf-8 -*-

"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__csrc.py
    Description:    行政处罚 - 中国证券监督管理委员会
    Author:         QL
    Date:           2017-09-18
    version:        v.1.0
-------------------------------------------------
"""

import math
import re
import traceback

from lxml.html.clean import Cleaner
from scrapy import Request
from scrapy.selector import Selector

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_strip
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzxk.field_mapping import map_field


class Crawler__qyxg_xzcf__csrc(SpiderAll):
    """
    行政处罚 - 中国证券监督管理委员会
    """
    name = 'Crawler__qyxg_xzcf__csrc'
    start_urls = ['http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401.htm']

    def custom_init(self, *args, **kwargs):
        self.cleaner = Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)

    def parse(self, response):
        try:
            self.logger1.info("start to get pages info")
            total_records = int(re.search(r'var m_nRecordCount = "(\d+)";', response.text).group(1))
            pages = int(math.ceil(total_records / 20.0))
            self.logger1.info("it has {} pages".format(pages))
            for req in self.get_list(response):
                yield req
            base_url = 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401_{}.htm'
            for page in range(1, pages):
                url = base_url.format(page)
                yield Request(url, callback=self.get_list, errback=self.err_get_list,
                              dont_filter=True, meta={'pn': page + 1})
        except:
            err_msg = "fail to get pages: {}".format(traceback.format_exc())
            self.logger1.error(err_msg)

    def get_list(self, response):
        try:
            self.logger1.info("start to get the {} page".format(response.meta.get('pn', 1)))
            all_hrefs = response.xpath('//li[@class="mc"]//a/@href').extract()
            if not all_hrefs:
                raise Exception("the web page has changed in {}, please check".format(response.url))
            for href in all_hrefs:
                url = response.urljoin(href)
                yield Request(url, callback=self.parse_item, errback=self.err_parse_item)
        except:
            err_msg = "fail to get results: {}".format(traceback.format_exc())
            self.logger1.error(err_msg)

    def parse_item(self, response):
        try:
            self.logger1.info("start to parse detail page: {}".format(response.url))
            table = response.xpath('//table[@id="headContainer"]')
            if not table:
                raise Exception("the web page has changed in {}, please check".format(response.url))
            tds_raw_text = [''.join(td.xpath('.//text()').extract()).strip()
                            for td in table.xpath('.//td[@colspan="2"]//td')]
            part_result = {}
            for text in tds_raw_text:
                try:
                    key, value = re.split(r'：|:', text, 1)
                    part_result[clean_all_space(key)] = value.strip()
                except:
                    self.logger1.error("can't split it by ':': {}".format(text))
            part_result['案件名称'] = xpath_extract_text_strip(response, '//span[@id="lTitle"]')
            part_result['标题'] = part_result['案件名称']
            main_div = self.cleaner.clean_html(response.xpath('//div[@id="ContentRegion"]').extract()[0])
            slt = Selector(text=main_div)
            part_result['正文'] = xpath_extract_text_strip(slt, '//div[@id="ContentRegion"]')
            yield self.handle_result(response, part_result)
            self.logger1.info("store data to database successfully!")
        except:
            err_msg = "fail to get detail info: {}".format(traceback.format_exc())
            self.logger1.error(err_msg)

    def handle_result(self, response, result_dict):
        result = map_field(result_dict)
        item = self.result_item_assembler(response)
        item['_parsed_data'] = result
        item['bbd_html'] = ''
        return item

    def err_get_pages(self, response):
        self.logger1.error("failed to get pages: {}".format(response.request.url))

    def err_get_list(self, response):
        self.logger1.error("failed to get results: {}".format(response.request.url))

    def err_parse_item(self, response):
        self.logger1.error("failed to parse detail info: {}".format(response.request.url))
