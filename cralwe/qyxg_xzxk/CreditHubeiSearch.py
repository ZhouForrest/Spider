# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditHubeiSearch.py
    Description:    双公示-信用湖北-基类-搜索
    Author:         Abby
    Date:           2018-01-09
    Version:        v.1.0

    Lastmodified:       2018-01-09  by  Abby
-------------------------------------------------
"""
import copy
import datetime
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


class CreditHubeiSearch(Spider_Seed):
    """
    双公示-信用湖北-基类
    """

    name = "CreditHubeiSearch"

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
        form_data.update({"bt": data})
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
            page_str = ''.join(response.xpath(".//script").xpath("string(.)").extract())
            page_count = int(re.findall('var totalPages = (\d+)', page_str)[0])
            if page_count == 0:
                self.logger1.info("当前种子{}搜索结果为空".format(key))
                return
            form_data = copy.deepcopy(self.form_data)
            for page in range(1, page_count + 1):
                form_data.update({"bt": key, "pageIndex": "{}".format(page)})
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
            self.logger1.info(
                "Start to parse page {} the detail link of {}".format(response.meta.get("page", 1), response.url))
            link_list = list(set(response.xpath(".//div[@class='right_xkgs']//table//tr//td//a//@href").extract()))
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
            tr_list = response.xpath("//div[@class='display_con']//table//tr[position()>1]")
            data_dict = {}
            title_list = []
            value_list = []
            for tr in tr_list:
                tds = tr.xpath(".//td")
                title_list += [clean_all_space(''.join(td.xpath("string(.)").extract())) for td in tds[::2]]
                value_list += [clean_all_space(''.join(td.xpath("string(.)").extract())) for td in tds[1::2]]
            data_dict.update(dict(zip(title_list, value_list)))
            item = ParsedItem()
            self.common_item_assembler(response, item)
            item["_id"] = "{}_{}".format(response.url, uuid.uuid4())
            item['bbd_html'] = ''
            item['bbd_type'] = "credit_hb"
            item['rowkey'] = gen_rowkey(item, keys=('do_time', 'bbd_type'))
            result_dict = map_field(data_dict)
            if "xzcf" in self.bbd_table:
                result_dict["punish_status"] = result_dict.pop("license_status", "")
            item['_parsed_data'] = self.convert_time(result_dict)
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