# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__credit_wuxi_base.py

    Description:      信用巫溪-行政许可&行政处罚

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-21-14:55:06

    Version:          v1.0

    Lastmodified:     2018-08-21 by Jack Deng

-------------------------------------------------
"""

import re
import json
import traceback

from math import ceil
from scrapy import Request, FormRequest

from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__credit_wuxi_base(Spider):
    """
    class Crawler__credit_wuxi_base for
    信用奉节-行政许可&行政处罚 基类
    """

    name = "Crawler__credit_wuxi_base"
    page_url = ""
    detail_url = ""
    specific_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spiders.middleware.filterkeywordsmiddleware.FilterKeywordsMiddleware': 300
        },
    }
    filter_keywords_for_page = {
        'http://wuxi.hlxy.com/documents/api/queryCreditPublicity?pageNum=.*&typeCode=300008&keyWord=': {
            'pass_key_word': [''],
        },
    }

    def get_ext_requests_or_urls(self):
        """
        custom first request
        :Keyword Arguments:
         self --
        :return: None
        """
        return Request(
            url=self.page_url.format("1"),
            dont_filter=True,
            callback=self.parse,
            errback=self.err_parse
        )

    def parse(self, response):
        """
        parse first page and get all pageNum
        :Keyword Arguments:
         self     --
         resposne --
        :yield: turn page requests
        """
        try:
            for req in self.parse_list(response):
                yield req
            json_data = json.loads(response.text)
            total_page = int(json_data["data"]["totalPage"])
            for page in range(2, total_page+1):
                yield Request(
                    url=self.page_url.format(page),
                    dont_filter=True,
                    callback=self.parse_list,
                    errback=self.err_parse,
                    meta={"page": page}
                )
                self.logger1.info("yield turn page {}".format(page))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to parse page {page}, url {url} error:{err_msg}".
                format(page=page, url=response.url, err_msg=err_msg))

    def parse_list(self, response):
        """
        parse each list and yield detail requests
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page = response.meta.get("page", 1)
            json_data = json.loads(response.text)
            data_list = json_data["data"]["data"]
            id_list = [(x["id"], x["orgName"])for x in data_list]
            for id_name in id_list:
                detail_id, name = id_name
                yield Request(
                    url=self.detail_url.format(detail_id),
                    callback=self.save_detail,
                    errback=self.err_parse,
                    meta={
                        "name": name,
                        "page": page,
                    }
                )
                self.logger1.info("page {} yield detail name {}".format(page, name))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to parse page {page}, url {url} error:{err_msg}".
                format(page=page, url=response.url, err_msg=err_msg))

    def save_detail(self, response):
        """
        save detail page to ssdb
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page, name = response.meta["page"], response.meta["name"]
            status, item = self.source_item_assembler(response)
            if status:
                yield item
                self.logger1.info("page {} save to ssdb".format(
                    page, name))
            else:
                self.logger1.warning("page {} save failed".format(
                    page, name))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to parse page {page}, url {url} error:{err_msg}".
                format(page=page, url=response.url, err_msg=err_msg))

    def err_parse(self, failure):
        self.logger1.warning('failed request page: {}'.format(
            failure.request.url))
