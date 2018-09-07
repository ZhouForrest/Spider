#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: sc_l_base_crawl.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-26 17:19
:Version: v.1.0
:Description: 
"""
import re
from scrapy.http.request import Request
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class SCLocalBaseCrawl(Spider):
    """四川省地方税务局-税务行政处罚公告数据 - base"""
    name = 'SCLocalBaseCrawl'
    
    start_urls = ['http://zg.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index.html']
    
    next_page_tpl = 'http://zg.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index_{}.html'
    
    _result_pop_key_list = ['_request_url', '_method', '_header', '_response_url']
    
    def parse(self, response):
        page_script_str = response.xpath('string(//div[@class="p_list_next f14"])').extract_first()
        page_script_str = re.sub('\s+', '', page_script_str)
        total_page_re = re.match('.*page\',(\d+),\d+,(\d+).*', page_script_str)
        if total_page_re:
            total_page = int(total_page_re.groups()[0])
            cur_page = int(total_page_re.groups()[1])
            self.logger.log_more('total page: {}, cur page:{}'.format(total_page, cur_page))
            if cur_page < total_page - 1:
                next_page = cur_page + 1
                self.logger.log_more('send pagination request {}:'.format(self.next_page_tpl.format(next_page)))
                yield Request(url=self.next_page_tpl.format(next_page), callback=self.parse, dont_filter=True)
        detail_script_str = re.sub('\s+', '', ''.join(response.xpath('//div[@class="contR fr"]//script').extract()))
        detail_page_list = re.findall('href="(.*?/\d+/\w+\d+_\d+\.html)', detail_script_str)
        
        if detail_page_list and isinstance(detail_page_list, list):
            detail_page_list = list(set(detail_page_list))
            self.logger1.log_more(
                'Current url: {}, detail length:{}'.format(response.request.url, len(detail_page_list)))
            for detail_url in detail_page_list:
                final_detail_url = response.urljoin(detail_url)
                yield Request(url=final_detail_url, callback=self.parse_detail)
    
    def parse_detail(self, response):
        status, source_item = self.source_item_assembler(response)
        yield source_item