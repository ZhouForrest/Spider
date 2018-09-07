# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd


    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__qyxg_xzcf__credit_dongying.py

    Description:      信用中国（东营）- 行政处罚

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-06-09:39:37

    Version:          v1.0

    Lastmodified:     2018-08-06 by Jack Deng
-------------------------------------------------
"""

import re
import json
import traceback

from math import ceil
from scrapy import Request, FormRequest

from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__qyxg_xzcf__credit_dongying(Spider):
    """
    class Crawler__qyxg_xzcf__credit_dongying for
    信用中国（东营）- 行政处罚
    """

    name = "Crawler__qyxg_xzcf__credit_dongying"
    post_url = "http://credit.dongying.gov.cn/creditInquiry/xzcfLZ"
    detail_format = "http://credit.dongying.gov.cn/creditInquiry/xzcfLZxq?id={}"
    form_data = {
        "dept": "",
        "name": "",
        "pageSize": "100",
        "pageNo": "1",
    }

    def get_ext_requests_or_urls(self):
        """

        :Keyword Arguments:
         self --
        :return: None
        """
        return FormRequest(
            url=self.post_url,
            dont_filter=True,
            formdata=self.form_data,
            callback=self.parse,
            errback=self.err_parse)

    def parse(self, response):
        """
        parse to get page num and yield turn page
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            for req in self.parse_list(response):
                yield req
            json_data = json.loads(response.text)
            total = int(json_data["total"])
            pages = ceil(total / int(self.form_data["pageSize"]))
            for page in range(2, pages + 1):
                self.form_data["pageNo"] = "{}".format(page)
                yield FormRequest(
                    url=self.post_url,
                    dont_filter=True,
                    formdata=self.form_data,
                    callback=self.parse_list,
                    errback=self.err_parse,
                    meta={"page": page}
                )
                self.logger1.info("yield turn page {}".format(page))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to parse first page, url {url} error:{err_msg}".format(
                    url=response.url, err_msg=err_msg))

    def parse_list(self, response):
        """
        parse each page and yield detail page
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page = response.meta.get("page", 1)
            json_data = json.loads(response.text)
            for each in json_data["results"]:
                detail_url = self.detail_format.format(each["ID"])
                company_name = each["LEGALPERSON"]
                yield Request(
                    url=detail_url,
                    callback=self.save_detail,
                    errback=self.err_parse,
                    meta={
                        "page": page,
                        "name": company_name
                    })
                self.logger1.info("page {} yield detail name {}".format(
                    page, company_name))
        except Exception:
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
                self.logger1.info("page {} name {} save successed".format(
                    page, name))
            else:
                self.logger1.warning("page {} name {} save failed".format(
                    page, name))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to save detail page {page}, name {name}, url {url} error:{err_msg}".
                format(
                    page=page, name=name, url=response.url, err_msg=err_msg))

    def err_parse(self, failure):
        self.logger1.warning('failed request page: {}'.format(
            failure.request.url))
