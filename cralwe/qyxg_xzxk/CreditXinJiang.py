# -*- coding:utf8 -*-

"""
-------------------------------------------------
    Copyright:      2017, BBD Tech. Co.,Ltd.
    File Name:      CreditXinJiang.py
    Description:    信用新疆 - 行政许可&行政处罚
    Author:         QL
    Date:           2017-12-20
    Version:        v.1.0
-------------------------------------------------
"""

import copy
import re
import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_strip
from hive_framework_milk.commons.utils.selector_util import convert_formal_date
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditXinJiang(SpiderAll):
    """
    信用新疆 - 行政许可&行政处罚
    """
    name = 'CreditXinJiang'
    detail_url = post_url = ''
    form_data = {
        "pageNum": "",
        "numPerPage": "10",
        "orderField": "",
        "orderDirection": "",
        "prePage": "1",
        "nextPage": "3",
        "ttPage": "",
    }

    def custom_init(self, *args, **kwargs):
        if not self.detail_url or self.post_url:
            raise NotImplementedError('please make sure detail_url or post_url is not empty')

    def parse(self, response):
        """
        get pages and request all the list-pages.
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse initial url:{}'.format(response.url))
            total_pages = int(response.xpath('//input[@id="totalPage"]/@value').extract_first())
            self.logger1.info('total pages: {}'.format(total_pages))
            self.form_data['ttPage'] = str(total_pages)

            for page in range(2, total_pages + 1):
                form_data = copy.deepcopy(self.form_data)
                form_data["pageNum"] = str(page)
                yield FormRequest(self.post_url, callback=self.parse_list, errback=self.err_parse_list,
                                  formdata=form_data, dont_filter=True, meta={'page_num': page})

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
            trs = response.xpath('//td[text()="案件名称"]/../../tr')
            if not trs:
                raise Exception("the web page maybe change in {}, please check".format(response.url))
            urls_list = trs.xpath('.//a/@href').extract()

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
            all_lis = response.xpath('//div[@class="warp"]//li')
            if not all_lis:
                raise Exception('this page has changed! please check {}'.format(response.url))
            result_dict = {}
            for li in all_lis:
                key = re.sub(r':|：', r'', clean_all_space(''.join(li.xpath('./text()').extract())))
                value = xpath_extract_text_strip(li, './span')
                if '身份证' in key:
                    value = clean_all_space(value)
                if key.endswith(('期', '戳')):
                    # 许可决定日期、许可截止期、处罚决定日期、数据时间更新戳 等等
                    _, value = convert_formal_date(value, need_time=True)
                    if len(value) == 16:
                        value += ':00'
                    elif len(value) == 10:
                        value += ' 00:00:00'
                result_dict[key] = value
            yield self.handle_result(response, result_dict)
            self.logger1.info("store data to database successfully!")
        except:
            err_msg = traceback.format_exc()
            self.logger.warning("failed to parse detail page, url {url} error:{err_msg}"
                                .format(url=response.url, err_msg=err_msg))

    def handle_result(self, response, result_dict):
        item = self.result_item_assembler(response)
        item['_parsed_data'] = map_field(result_dict)
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_params'] = ''
        return item

    def err_parse_detail(self, failure):
        self.logger1.warning('failed to request detail page: {}'.format(failure.request.url))

    def err_parse_list(self, failure):
        self.logger1.error("failed to get list-page's results: {}".format(failure.request.url))
