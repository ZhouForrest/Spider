#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__cd_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 10:39
:Version: v.1.0
:Description: 
"""

import json
import math

from scrapy.utils.url import urlparse
from scrapy.http.request import Request
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__qyxg_xzcf__cd_l_tax(Spider):
    """四川省地方税务局-税务行政处罚公告数据 - 成都"""
    name = 'Crawler__qyxg_xzcf__cd_l_tax'
    
    pagination_url_template = 'http://cd.sc-l-tax.gov.cn/cpthd_cd/search_scds/findPages.action?pageSize={}' \
                              '&pageNumber={}&siteid=13&channlid=9396&keycontent=1&keytitle=1'

    specific_settings = {'RETRY_TIMES': 100}
    
    def parse(self, response):
        """
        Json data, pagination.
        :param response:
        :return:
        """
        _parsed_url = urlparse(response.url)
        assemble_f = lambda query: {_item.split('=')[0]: _item.split('=')[1] \
            if len(_item.split('=')) >1 else '' for _item in query.split('&')}
        parsed_query_dict = assemble_f(_parsed_url.query)
        _page_size = int(parsed_query_dict['pageSize'])
        _page_number = int(parsed_query_dict['pageNumber'])
        try:
            response_body_dict = json.loads(response.text)
        except:
            self.logger1.log_more('json loads failed, {}'.format(response.body))
            response_body_dict = json.loads(response.xpath('//pre/text()').extract_first())
        _total_count = response_body_dict.get('total')
        
        for item in response_body_dict['rows']:
            yield Request(url=item['url'], callback=self.parse_detail)
        
        _total_page = math.ceil(_total_count / _page_size)
        self.logger1.log_more('Total count: {}, current page:{}, page_size:{}, pages left:{}'.format(
            _total_count, _page_number, _page_size, _total_page - _page_number
        ))
        if _total_page > _page_number:
            _page_number += 1
            next_page_url = self.pagination_url_template.format(_page_size, _page_number)
            self.logger1.log_more('Send next page url: {}'.format(next_page_url))
            yield Request(url=next_page_url, dont_filter=True)
        else:
            self.logger1.log_more('Pagination end.')
            
    def parse_detail(self, response):
        """
        Save source
        :param response:
        :return:
        """
        status, item = self.source_item_assembler(response)
        yield item