# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditAnhui.py
    Description:    信用安徽
    Author:         hyy
    Date:           2017-12-28
    version:        v.1.0
-------------------------------------------------
"""
import json
import re
import json
import traceback

from scrapy.http.request import Request

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditAnhui(SpiderAll):
    """
    Credit an hui info base class.
    """
    name = 'CreditAnhui'

    def parse(self, response):
        try:
            page_count = json.loads(response.text).get('page', {}).get('totalPage', 0)
            for page in range(1, page_count + 1):
                url = response.url + "&pageNo={}&pageSize=10".format(page)
                yield Request(url, callback=self.parse_page, errback=self.error_parse,
                              dont_filter=True, meta={'page_count': page_count})
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_page(self, response):
        """
        parse detail page link
        :param response:
        :return:
        """
        try:
            self.logger1.info("Start to parse the detail link of {}".format(response.url))
            data_list = json.loads(response.text).get('data', [])
            for data in data_list:
                yield Request(data.get('url', ''), callback=self.parse_detail, errback=self.error_parse)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on parse the link page[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        """
        parse detail page
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse {}'.format(response.url))
            tr_list = response.xpath("//table[@class='infor']//tr")
            if tr_list:
                data_dict = {}
                result = {}
                for tr in tr_list:
                    title = ''.join(tr.xpath(".//td[@class='name']/text()").extract()
                                    ).strip().replace('：', '').replace(':', '').strip()
                    value = ''.join(tr.xpath(".//td[last()]").xpath("string()").extract()).strip()
                    if title in ['处罚类别', '处罚类型']:
                        if '处罚类别1' in data_dict.keys():
                            title = '处罚类别2'
                        else:
                            title = '处罚类别1'
                    data_dict.update({title: value})
                data_dict[self.data_status] = data_dict.pop('当前状态', '')

                result.update(map_field(data_dict))
                for key, value in result.items():
                    if 'date' in key:
                        if value.strip().isdigit():
                            val = '{}-{}-{} 00:00:00'.format(value[:4], value[4:6], value[6:])
                        elif ':' in value:
                            val = '-'.join(re.findall(r'(\d+)', value.split(' ')[0])) + ' {}'.format(value.split(' ')[1])
                        else:
                            val = '-'.join(re.findall(r'(\d+)', value)) + ' 00:00:00' if value else ''
                        result[key] = val
                item = self.result_item_assembler(response)
                item['_id'] = calc_str_md5(response.url)
                item['bbd_html'] = ''
                item['_parsed_data'] = result
                yield item
                self.logger1.info('{} save successfully'.format(response.url))
            else:
                self.logger1.info("retry {}".format(response.url))
                yield Request(response.url, callback=self.parse_detail, errback=self.error_parse)

        except Exception as e:
            self.logger1.warning("Exception on save detail page {} {} {}".format(
                response.url, traceback.format_exc(), e))

    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
