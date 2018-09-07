# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditGuizhou.py
    Description:    信用贵州
    Author:         Abby
    Date:           2017-12-19
    Version:        v.1.0
    LastModified:   2018-02-24  by  Jack Deng 双公示行政处罚　bugfix 修改"license_status" 为　"punish_status"
-------------------------------------------------
"""
import copy
import datetime
import re
import time
import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditGuizhou(SpiderAll):
    """
    Credit fu jian info base class.
    """
    name = 'CreditGuizhou'

    def parse(self, response):
        try:
            page_str = clean_all_space("".join(response.xpath("//*[@class='pageinfo']").xpath("string(.)").extract()).strip())
            page_count = int(re.findall(r'共(\d+)页', page_str)[0])
            yield Request(response.url, callback=self.parse_link, errback=self.error_parse, dont_filter=True)
            for page in range(2, page_count + 1):
                form_data = copy.deepcopy(self.form_data)
                form_data.update({"pageNo": "{}".format(page)})
                yield FormRequest(self.post_url, formdata=form_data, callback=self.parse_link,
                                  errback=self.error_parse, dont_filter=True)
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
            self.logger1.info("Start to parse the detail link of {}".format(response.url))
            link_list = response.xpath(".//ul")[-1].xpath(".//li//a//@href").extract()
            for link in link_list:
                detail_url = response.urljoin(link.strip())
                yield Request(detail_url, callback=self.parse_detail, errback=self.error_parse)
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
            tr_list = response.xpath("//table[@class='table_normal1']//tr")
            data_dict = {}
            for tr in tr_list:
                title = ''.join(tr.xpath(".//th").xpath("string()").extract()).strip()
                value = ''.join(tr.xpath(".//td").xpath("string()").extract()).strip()
                data_dict.update({title: value})
            item = self.result_item_assembler(response)
            item['_id'] = calc_str_md5(response.url)
            item['bbd_html'] = ''
            res_dict = self.convert_time(map_field(data_dict))
            if "xzcf" in self.name and "license_status" in res_dict.keys():
                    res_dict["punish_status"] = res_dict.pop("license_status", "")
            item['_parsed_data'] = res_dict
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
