# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditHainan.py
    Description:    信用海南
    Author:         Abby
    Date:           2017-12-19
    version:        v.1.0
-------------------------------------------------
"""
import datetime
import json
import re
import time
import traceback

from lxml import etree
from scrapy.http.request import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditHainan(SpiderAll):
    """
    Credit Hai nan info base class.
    """
    name = 'CreditHainan'

    def parse(self, response):
        try:
            data = json.loads(response.text)
            pages = data.get("pageLast", 1)
            for page in range(1, pages + 1):
                url = response.url.replace("pageIndex=1", "pageIndex={}".format(page))
                yield Request(url, callback=self.parse_link, errback=self.error_parse, dont_filter=True)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_link(self, response):
        """
        parse detail page link
        :param response:
        :return:
        """
        try:
            data = json.loads(response.text)
            data_list = data.get("data", [])
            for dt in data_list:
                url = self.detail_url.format(dt.get("uuid", ""))
                yield Request(url, callback=self.parse_detail, errback=self.error_parse)
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
            data = json.loads(response.text)
            html = data.get("contentViewsMap", "").get("rightData1", "")
            tree = etree.HTML(html)
            tr_list = tree.xpath(".//tr")
            title_list = []
            value_list = []
            for tr in tr_list[1:]:
                tds = tr.xpath(".//td")
                title_list += [''.join(td.xpath("string()")).strip() for td in tds[::2]]
                value_list += [''.join(td.xpath("string()")).strip() for td in tds[1::2]]
            data_dict = dict(zip(title_list, value_list))
            item = self.result_item_assembler(response)
            item['_id'] = calc_str_md5(response.url)
            item['bbd_html'] = ''
            item['_parsed_data'] = self.convert_time(map_field(data_dict))
            yield item
            self.logger1.info('{} save successfully'.format(response.url))
        except Exception as e:
            self.logger1.warning("Exception on save detail page {} {} {}".format(
                response.url, traceback.format_exc(), e))

    def convert_time(self, res_dict):
        res = {}
        for title, value in res_dict.items():
            if "date" in title:
                if len(clean_all_space(value)) in [10, 11]:
                    d_time = re.sub("[\u4e00-\u9fa5]|/|-", "-", clean_all_space(value)).strip("-")
                    t = time.strptime(d_time, "%Y-%m-%d")
                    y, m, d = t[0:3]
                    res.update({title: str(datetime.datetime(y, m, d))})
                else:
                    res.update({title: value})
            else:
                res.update({title: value})
        return res

    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
