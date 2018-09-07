# -*- coding:utf8 -*-

"""
-------------------------------------------------
    Copyright:      2017, BBD Tech. Co.,Ltd.
    File Name:      CreditGanSu.py
    Description:    信用甘肃 - 行政许可&行政处罚
    Author:         QL
    Date:           2018-01-05
    Version:        v.1.0
-------------------------------------------------
"""

import re
import traceback

from scrapy import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_no_spaces
from hive_framework_milk.commons.utils.selector_util import convert_formal_date
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditGanSu(SpiderAll):
    """
    信用甘肃 - 行政许可&行政处罚
    """
    name = 'CreditGanSu'

    def parse(self, response):
        """
        get pages and request all the list-pages.
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse initial url:{}'.format(response.url))
            script_text = xpath_extract_text_no_spaces(response, '//script')
            total_pages = int(re.search(r'pages:(\d+)', script_text).group(1))
            self.logger1.info('total pages: {}'.format(total_pages))

            base_page_url = response.url.replace('/list.', '/list_{}.')
            for page in range(2, total_pages + 1):
                url = base_page_url.format(page)
                yield Request(url, callback=self.parse_list, errback=self.err_parse_list,
                              dont_filter=True, meta={'page_num': page})

            # 发出第一页中的列表URL的请求
            for req in self.parse_list(response):
                yield req
        except:
            self.logger1.warning('parse list pages wrong: {}'.format(traceback.format_exc()))

    def parse_list(self, response):
        """
        Parse the list pages: get the pubdate and target url.
        :param response:
        :return:
        """
        try:
            page_num = response.meta.get('page_num', 1)
            self.logger1.info('parse the {} page now'.format(page_num))
            urls_list = response.xpath('//div[@class="company-messages"]//a/@href').extract()
            assert urls_list, "don't get the urls list, please check xpath: {]".format(response.url)

            for url in set(urls_list):
                url = response.urljoin(url.strip())
                yield Request(url, callback=self.parse_detail, errback=self.err_parse_detail)
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
            request_count = response.meta.get('request_count', 1)
            keys = response.xpath('//p[@class="tab1-p-left"]/text()').extract()
            assert keys, "this page has changed, please check xpath: {]".format(response.url)
            keys = [re.sub(r':|：', '', key) for key in keys]
            values = response.xpath('//p[@class="tab1-p-right"]').xpath('string()').extract()
            result_dict = dict(zip(keys, values))
            for key, value in result_dict.items():
                if key.endswith(('期', '戳')):
                    # 许可生效期、许可截止期、公示日期 等等
                    _, value = convert_formal_date(value, need_time=True)
                    if len(value) == 10:
                        value += ' 00:00:00'
                    result_dict[key] = value

            # 如果没有抓到有效的数据，则重新请求该详情页，至多10次
            if not clean_all_space(''.join(result_dict.values())):
                if request_count < 10:
                    self.logger1.warning("the parsed data was empty, so request again!")
                    yield Request(response.url, callback=self.parse_detail, errback=self.err_parse_detail,
                                  dont_filter=True, meta={'request_count': request_count + 1})
                else:
                    self.logger1.warning("this page has requested more than 10 times, ignore it!")
            else:
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

    def err_parse_list(self, failure):
        self.logger1.error("failed to get list-page's results: {}".format(failure.request.url))
