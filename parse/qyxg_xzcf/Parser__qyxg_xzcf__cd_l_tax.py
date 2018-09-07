#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__cd_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from scrapy.selector import Selector
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__cd_l_tax(SC_l_tax_base):
    """成都  只保留原文"""

    def parse(self, source, *args, **kwargs):
        html = source.get('bbd_html')
        response = Selector(text=html)
    
        data = {}
        pub_date_str = response.xpath('string(//div[@class="time"])').extract_first()
        pub_date_re_result = re.match('.*(\d{4}-\d{2}-\d{2}).*', pub_date_str)
        if pub_date_re_result:
            pub_str = pub_date_re_result.groups()[0].replace('-', '/')
            data['pubdate'] = pub_str
        else:
            self.logger.log_more('pub_date parse failed', level='warn')
        title = response.xpath('string(//div/h1[@class="f24 fontWr"])').extract_first()
        if title:
            data['title'] = title.strip()
        else:
            self.logger.log_more('title parse failed', level='warn')
    
        source['bbd_html'] = ''
        source['_dup_str'] = source['bbd_url']
        source['bbd_params'] = ''
        source['content_html'] = self._get_content_html(response)
        return source
    
    def _get_content_html(self, response):
        # get content_html,
        # git content with html tags.
        plain_html_str = ''.join(response.xpath('//div[@class="p_dis_main"]').extract()) or \
                         ''.join(response.xpath('//div[@id="p_dis_wiap"]').extract()) or\
                         ''.join(response.xpath('.').extract())
        return plain_html_str