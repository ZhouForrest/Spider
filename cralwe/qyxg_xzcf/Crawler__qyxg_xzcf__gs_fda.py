# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        specific_spiders/qyxg_xzcf/Crawler__qyxg_xzcf__gs_fda.py

    Description:      xzcf-甘肃省食品药品监管局

    Author:           dengliangwen@bbdservice.com

    Date:             2018-05-07-14:36:08

    Version:          v1.0

    Lastmodified:     2018-05-07 by Jack Deng

-------------------------------------------------
"""

import re
import traceback

from math import ceil
from scrapy import Request

from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__qyxg_xzcf__gs_fda(Spider):
    """
    class Crawler__qyxg_xzcf__gs_fda for xzcf-甘肃省食品药品监管局
    """

    name = "Crawler__qyxg_xzcf__gs_fda"
    start_urls = [
        "http://apps.gsfda.gov.cn:2180/xzlaw/xzlawActionWZ!list.do?queryBean.pn=1&queryBean.pageSize=100"
    ]
    turn_page_format = "http://apps.gsfda.gov.cn:2180/xzlaw/xzlawActionWZ!list.do?queryBean.pn={}&queryBean.pageSize=100"
    specific_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spiders.middleware.filterkeywordsmiddleware.FilterKeywordsMiddleware': 300
        },
    }
    filter_keywords_for_page = {
        'http://apps.gsfda.gov.cn:2180/xzlaw/xzlawActionWZ!show.do\?dbAdministrative.id=.*': {
            'key_word_xpath': "//html//body//table//tr//text()",
            'pass_key_word': [''],
        },
    }

    def parse(self, response):
        """
        parse first page to get page num, and yield turn page
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            for req in self.parse_list(response):
                yield req
            all_data_num = int(
                re.search(r'var\s+p\s+=\s+new\s+Pagination\((\d+),.*',
                          response.text).group(1))
            pages = int(ceil(all_data_num / 100))
            for page in range(2, pages + 1):
                url = self.turn_page_format.format(page)
                yield Request(
                    url=url,
                    dont_filter=True,
                    callback=self.parse_list,
                    errback=self.err_parse,
                    meta={"page": page})
                self.logger1.info("yield turn page {}".format(page))
        except Exception as err:
            self.logger1.warning('parse first page wrong: {}'.format(
                traceback.format_exc()))

    def parse_list(self, response):
        """
        parse each page and yield detail request
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page = response.meta.get("page", 1)
            trs = response.xpath('//table[@id="list"]//tr[position()>1]')
            hrefs = [
                "".join(tr.xpath('.//td[last()]//a/@href').extract()).strip()
                for tr in trs
            ]
            for href in hrefs:
                req_url = response.urljoin(href)
                yield Request(
                    url=req_url,
                    callback=self.save_detail,
                    errback=self.err_parse,
                    meta={
                        "page": page,
                    })
                self.logger1.info("page {} yield detail req {}".format(
                    page, req_url))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger.warning(
                "failed to parse list page, url {url} error:{err_msg}".format(
                    url=response.url, err_msg=err_msg))

    def save_detail(self, response):
        """
        save detail page to ssdb
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page = response.meta["page"]
            self.logger1.info("start parse page {} url {}".format(
                page, response.url))
            status, item = self.source_item_assembler(response)
            if status:
                yield item
                self.logger1.info("page {} saved to ssdb".format(
                    page))
            else:
                self.logger1.warning(
                    "page {} url {} assembler failed, please check".
                    format(page, response.url))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger.warning(
                "failed to parse detail page {page}, url {url} error:{err_msg}"
                .format(
                    page=page, url=response.url, err_msg=err_msg))

    def err_parse(self, failure):
        self.logger1.warning('failed request page: {}'.format(
            failure.request.url))
