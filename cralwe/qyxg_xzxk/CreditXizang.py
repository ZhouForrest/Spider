# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditXizang.py
    Description:    信用西藏
    Author:         Abby
    Date:           2017-12-20
    version:        v.1.0
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


class CreditXizang(SpiderAll):
    """
    Credit xi zang info base class.
    """
    name = 'CreditXizang'

    def parse(self, response):
        try:
            page_count = int(clean_all_space(''.join(response.xpath(".//*[@id='pageForm']//input[contains(@name, 'ttPage')]//@value").extract())))
            form_data = copy.deepcopy(self.form_data)
            form_data.update({"ttPage": "{}".format(page_count)})
            for page in range(1, page_count + 1):
                if page == 1:
                    yield Request(response.url, callback=self.parse_link, errback=self.error_parse, dont_filter=True)
                else:
                    form_data.update({"pageNum": "{}".format(page), "prePage": "{}".format(page-1), "nextPage": "{}".format(page)})
                    yield FormRequest(self.post_url, formdata=form_data, meta={"page": page}, callback=self.parse_link, errback=self.error_parse, dont_filter=True)
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
            self.logger1.info("Start to parse page {} the detail link of {}".format(response.meta.get("page", 1), response.url))
            link_list = list(set(response.xpath(".//div[@id='content']//table//tr//td//a//@href").extract()))
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
            li_list = response.xpath("//div[@class='warp']//ul//li")
            data_dict = {}
            for li in li_list:
                data_str = clean_all_space(''.join(li.xpath("string()").extract()).replace("：", ":"))
                title = data_str.split(":", 1)[0]
                value = ''.join(li.xpath(".//span").xpath("string()").extract()).strip()
                data_dict.update({title: value})
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
