# -*- coding:utf8 -*-

"""
-------------------------------------------------
    Copyright:      2017, BBD Tech. Co.,Ltd.
    File Name:      CreditTianJin.py
    Description:    信用天津 - 行政许可&行政处罚
    Author:         QL
    Date:           2017-12-1
    Version:        v.1.0
-------------------------------------------------
"""

import re
import traceback

from scrapy import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_strip
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditTianJin(SpiderAll):
    """
    信用天津 - 行政许可&行政处罚
    """
    name = 'CreditTianJin'
    detail_url = ''
    total_datas = 0

    def parse(self, response):
        """
        get pages and request all the list-pages.
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse initial url:{}'.format(response.url))
            self.total_datas = int(''.join(response.xpath('//label[@id="tabSum"]/text()').extract()).strip())
            if not self.detail_url:
                raise NotImplementedError('please make sure detail_url is not empty')

            for index in range(1, self.total_datas + 100):
                yield Request(self.detail_url.format(index), callback=self.parse_detail,
                              errback=self.err_parse_detail, meta={'count': index})
        except:
            self.logger1.warning('parse list pages wrong: {}'.format(traceback.format_exc()))

    def parse_detail(self, response):
        """
        parse the detail page.
        :param response:
        :return:
        """
        try:
            self.logger1.info("start to parse detail page: {}".format(response.url))
            all_lis = response.xpath('//div[@class="gs_detail"]/ul/li')
            if not all_lis:
                raise Exception('this page has changed! please check {}'.format(response.url))
            result_dict = {}
            for li in all_lis:
                key = re.sub(r':|：', r'', clean_all_space(''.join(li.xpath('./text()').extract())))
                value = xpath_extract_text_strip(li, './label')
                if key.endswith('期'):
                    # 许可决定日期、许可截止期、处罚决定日期 等等
                    # 样例：   2017/6/13
                    if value:
                        year, month, day = re.findall(r'\d+', value)[:3]
                        value = '{}-{:0>2}-{:0>2} 00:00:00'.format(year, month, day)
                result_dict[key] = value
            yield self.handle_result(response, result_dict)
            self.logger1.info("store data to database successfully!")
        except:
            err_msg = traceback.format_exc()
            self.logger.warning("failed to parse detail page, url {url} error:{err_msg}"
                                .format(url=response.url, err_msg=err_msg))

    def handle_result(self, response, result_dict):
        result_dict = map_field(result_dict)
        if 'xzcf' in self.name and 'license_status' in result_dict:
            result_dict['punish_status'] = result_dict.pop('license_status', '')
            
        item = self.result_item_assembler(response)
        item['_parsed_data'] = result_dict
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_params'] = ''
        return item

    def err_parse_detail(self, failure):
        self.logger1.warning('failed to request detail page: {}'.format(failure.request.url))
