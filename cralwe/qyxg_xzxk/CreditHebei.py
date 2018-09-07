# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditHebei.py
    Description:    双公示-信用河北-基类
    Author:         Jack Deng
    Date:           2018-01-02
    Version:        v.1.0

    Lastmodified:       2018-01-02  by  Jack Deng
    Lastmodified:       2018-01-08  by  Jack Deng
-------------------------------------------------
"""

import traceback
import uuid

from scrapy.http.request import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_framework_milk.scrapy_spiders.item.parsed_item import ParsedItem
from hive_framework_milk.scrapy_spiders.spiders.spider_seed import Spider_Seed
from .field_mapping import map_field


class CreditHebei(Spider_Seed):
    """
    双公示-信用河北-基类
    """

    name = "CreditHebei"
    seed_key = None
    search_url = None

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
        search_url = self.search_url.format(data)
        self.logger1.info("Start search by {}".format(data))
        return Request(
            url=search_url,
            dont_filter=True,
            callback=self.parse,
            errback=self.common_errback,
            meta={'key': data}
        )

    def parse(self, response):
        """
        解析搜索结果页面，yield详情页请求
        :param response:
        :return:
        """
        try:
            key = response.meta["key"]
            # 取一页所有的url
            hrefs = [href.strip() for href in response.xpath("//table//tr//td//a/@href").extract()]
            if not hrefs:
                self.logger1.warning("key {} search failed, please check".format(key))
                return
            for href in hrefs:
                detail_url = response.urljoin(href)
                yield Request(
                    url=detail_url,
                    dont_filter=True,
                    callback=self.parse_detail,
                    errback=self.common_errback,
                    meta={"key": key}
                )
                self.logger1.info("yield detail url , key {}".format(key))
            next_page_href = "".join(response.xpath('//a[@class="next-page"]/@href').extract())
            if next_page_href:# 有下一页就翻页
                next_url = response.urljoin(next_page_href)
                yield Request(
                    url=next_url,
                    dont_filter=True,
                    callback=self.parse,
                    errback=self.common_errback,
                    meta={"key": key}
                )
                self.logger1.warning("yield turn page, key {}".format(key))
            else:
                self.logger1.info("key {} only has one page".format(key))
        except:
            err_msg = traceback.format_exc()
            self.logger1.error("Exception on search {url}, error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        try:
            key = response.meta["key"]
            titles_tds = response.xpath("//table//tr//td[1]")
            values_tds = response.xpath("//table//tr//td[last()]")
            titles = [clean_all_space(td.xpath("string(.)").extract()) for td in titles_tds]
            values = ["".join(td.xpath("string(.)").extract()).strip() for td in values_tds]
            if len(titles) != len(values):
                raise Exception("the length of titles and values are not equal, url {}".format(response.url))
            tmp_dict = dict(zip(titles, values))
            res_dict = map_field(tmp_dict)
            if "xzcf" in self.name:
                if "license_status" in res_dict.keys():
                    res_dict["punish_status"] = res_dict.pop("license_status", "")
            item = ParsedItem()
            self.common_item_assembler(response, item)
            item["_id"] = "{}_{}".format(key, uuid.uuid4())
            item["bbd_html"] = ""
            item["_parsed_data"] = res_dict
            item["rowkey"] = gen_rowkey(item, keys=('do_time', 'bbd_type'))
            yield item
            self.logger1.info("one data {} save to mongodb".format(key))
        except:
            err_msg = traceback.format_exc()
            self.logger1.error("Exception on detail {url}, error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def common_errback(self, response):
        """
        请求失败时输出日志
        :param response:
        :return:
        """
        self.logger1.error('request {} failed'.format(response.request.url))
