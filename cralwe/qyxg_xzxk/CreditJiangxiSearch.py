# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditJiangxiSearch.py
    Description:    双公示-信用江西-基类-搜索
    Author:         Abby
    Date:           2018-01-09
    Version:        v.1.0

    Lastmodified:   2018-01-09  by  Abby
    LastModified:   2018-02-24  by  Jack Deng 双公示行政处罚　bugfix 修改"license_status" 为　"punish_status"
-------------------------------------------------
"""
import copy
import datetime
import json
import re
import time
import traceback
import uuid

from scrapy import FormRequest
from scrapy.http.request import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_framework_milk.scrapy_spiders.item.parsed_item import ParsedItem
from hive_framework_milk.scrapy_spiders.spiders.spider_seed import Spider_Seed
from .field_mapping import map_field


class CreditJiangxiSearch(Spider_Seed):
    """
    双公示-信用江西-基类
    """

    name = "CreditJiangxiSearch"

    custom_settings = {
        'ITEM_PIPELINES': {
             'hive_framework_milk.scrapy_spiders.pipeline.result_pipeline.ResultPipeline': 300
        },
    }

    def custom_init(self, *args, **kwargs):
        """
        检查属性，添加种子队列
        :param args:
        :param kwargs:
        :return:
        """
        super().custom_init(*args, **kwargs)
        if not self.seed_key or not self.search_url:
            raise NotImplementedError("seed_key {} or search_url {} not implemented".format(
                self.seed_key, self.search_url
            ))
        self.seed_queue_names = [self.seed_key]

    def make_request_from_seed(self, data):
        """
        根据种子，产生请求
        :param data:
        :return:
        """
        if isinstance(data, bytes):
            data = data.decode()
        search_url = self.search_url
        self.logger1.info("Start search by {}".format(data))
        form_data = copy.deepcopy(self.form_data)
        form_data.update({"inpParam": data})
        return FormRequest(
            url=search_url,
            dont_filter=True,
            callback=self.parse,
            formdata=form_data,
            errback=self.error_parse,
            meta={'key': data}
        )

    def parse(self, response):
        key = response.meta.get("key", "")
        self.logger1.info("Parsing company {}".format(key))
        try:
            page_data = json.loads(response.text)
            page_count = page_data.get("page_count", 1)
            if page_count == 0:
                self.logger1.info("当前种子{}搜索结果为空".format(key))
                return
            form_data = copy.deepcopy(self.form_data)
            for page in range(1, page_count + 1):
                form_data.update({"page": "{}".format(page), "inpParam": key})
                yield FormRequest(response.url, formdata=form_data, meta={"page": page}, callback=self.parse_link,
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
            self.logger1.info("Start to parse page {} the detail link of {}".format(response.meta.get("page", 1), response.url))
            page_data = json.loads(response.text)
            id_list = page_data.get("list", [])
            for link in id_list:
                url = self.detail_url.format(link.get("id", ""))
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
            tr_list = response.xpath("//div[@class='fl ml20 mb10 mt10 f_yh']//table//tr")
            data_dict = {}
            for tr in tr_list:
                title = clean_all_space(''.join(tr.xpath(".//th").xpath("string(.)").extract()).replace("：", "").replace(":", ""))
                value = clean_all_space(''.join(tr.xpath(".//td").xpath("string(.)").extract()))
                data_dict.update({title: value})
            item = ParsedItem()
            self.common_item_assembler(response, item)
            item["_id"] = "{}_{}".format(response.url, uuid.uuid4())
            item['bbd_html'] = ''
            item['bbd_type'] = "credit_jx"
            item['rowkey'] = gen_rowkey(item, keys=('do_time', 'bbd_type'))
            res_dict = self.convert_time(map_field(data_dict))
            if "xzcf" in self.name:
                if "license_status" in res_dict.keys():
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
