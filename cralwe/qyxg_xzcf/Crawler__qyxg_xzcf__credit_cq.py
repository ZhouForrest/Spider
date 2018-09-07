# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_cq.py
    Description:    双公示-信用重庆-行政处罚爬虫
    Author:         crazy_jacky
    Date:           2018-01-02
    version:        v.1.0
-------------------------------------------------
"""

import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzxk.field_mapping import map_field


class Crawler__qyxg_xzcf__credit_cq(SpiderAll):
    """双公示-信用重庆-行政处罚爬虫"""
    name = 'Crawler__qyxg_xzcf__credit_cq'
    start_urls = ['http://www.xycq.gov.cn/html/query/punish/list.html']
    model_url = 'http://www.xycq.gov.cn/html/query/punish/detail.html?ids={}'

    def parse(self, response):
        """
        Args:
            response:
        Returns: the counts of pages
        """
        try:
            page_num = response.meta.get('page_num', 1)
            self.logger1.info("begin to parse home page")
            for item in self.parse_list(response):
                yield item
            url = response.url
            form_data = {'pageNo': '', 'contentType': '1'}
            is_end = response.xpath('.//td[@colspan="4"]')
            if not is_end:
                page_num += 1
                form_data.update({'pageNo': str(page_num)})
                yield FormRequest(url, formdata=form_data, callback=self.parse, errback=self.err_parse_list,
                                  dont_filter=True, meta={'page_num': page_num})
        except:
            err_msg = "fail to get pages: {}".format(traceback.format_exc())
            self.logger1.error(err_msg)

    def parse_list(self, response):
        """
        Args:
            response:
        Returns: the title,link and submit_date of each detail
        """
        try:
            page_num = response.meta.get('page_num', '1')
            self.logger1.info("start to parse list page detail id of page:{}".format(page_num))
            detail_id_lst = [item.split("'")[1] for item in response.xpath(".//td//a//@onclick").extract()]
            for detail_id in detail_id_lst:
                url = self.model_url.format(detail_id)
                yield Request(url, callback=self.parse_item, errback=self.err_parse_item)
            else:
                self.logger1.info('iter all detail page link in {}'.format(response.url))
        except:
            err_msg = "fail to get the detail page link in {}: {}".format(response.url, traceback.format_exc())
            self.logger1.error(err_msg)

    def parse_item(self, response):
        """
        Args:
            response:
        Returns: the details of each detail page
        """
        try:
            self.logger1.info("start to parse detail page: {}".format(response.url))
            count = response.meta.get('count', 0)
            key_lst = [item.strip(':') for item in response.xpath('.//td[@class="table_one_bgd"]//text()').extract()]
            val_lst = [''.join(item.xpath('string(.)').extract()).strip() for item in
                       response.xpath('.//td[@class="table_one_content"]')]
            if not any(val_lst):
                if count < 10:
                    count += 1
                    yield Request(response.url, callback=self.parse_item, errback=self.err_parse_item, meta={'count': count})
                else:
                    self.logger1.warn('url->"{}" had retried more than 10 times, so drop it')
                    return
            else:
                content_dict = dict(zip(key_lst, val_lst))
                result_dic = map_field(content_dict)
                yield self.handle_result(response, result_dic)
        except:
            err_msg = "fail to parse detail page in {}: {}".format(response.url, traceback.format_exc())
            self.logger1.error(err_msg)

    def handle_result(self, response, result_dict):
        """
        Args:
            response:
            result_dict:
        Returns:stored the detail items and mapping the english key
        """
        item = self.result_item_assembler(response)
        item['_parsed_data'] = result_dict
        item['bbd_html'] = ''
        return item

    def err_parse_list(self, response):
        self.logger1.error("failed to get results: {}".format(response.request.url))

    def err_parse_item(self, response):
        self.logger1.error("failed to parse detail info: {}".format(response.request.url))
