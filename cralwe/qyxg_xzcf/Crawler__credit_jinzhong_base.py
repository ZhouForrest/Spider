# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        specific_spiders/qyxg_xzcf/Crawler__credit_jinzhong_base.py

    Description:      信用晋中-行政许可&行政处罚 基类

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-06-11:24:43

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


class Crawler__credit_jinzhong_base(Spider):
    """
    class Crawler__credit_jinzhong_base for
    信用晋中-行政许可&行政处罚
    """

    name = "Crawler__credit_jinzhong_base"
    post_detail_urls = {}
    form_data = {
        "pageNo": "1",
    }
    specific_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spiders.middleware.filterkeywordsmiddleware.FilterKeywordsMiddleware': 300
        },
        'COOKIES_ENABLED': True
    }
    filter_keywords_for_page = {
        'http://www.creditsxjz.gov.cn/.*': {
            'key_word_xpath': '//body//text()',
            'pass_key_word': [''],
        },
    }

    def get_ext_requests_or_urls(self):
        """

        :Keyword Arguments:
         self --
        :return: None
        """
        res_list = []
        for post, detail in self.post_detail_urls.items():
            res_list.append(
                FormRequest(
                    url=post,
                    dont_filter=True,
                    formdata=self.form_data,
                    callback=self.parse,
                    errback=self.err_parse,
                    meta={"detail_format": detail}))
        return res_list

    def parse(self, response):
        """
        parse each page and yield turn next page
        :Keyword Arguments:
         self     --
         response --
        :return: None
        """
        try:
            page, detail_format = response.meta.get(
                "page", 1), response.meta["detail_format"]
            if "无数据" in response.text:
                self.logger1.warning("page {} is the last page".format(page))
                return
            detail_ids = response.xpath(
                '//div[@class="result-tab result-tab1 search-result-wrap "]//li//div[@onclick]/@onclick'
            ).extract()
            names = response.xpath(
                '//div[@class="result-tab result-tab1 search-result-wrap "]//li//div[@onclick]//h4//text()'
            ).extract()
            dealed_ids = list(
                map(lambda x: re.search(r"\(\'(.*)\'\)", x).group(1),
                    detail_ids))
            for name, detail in zip(names, dealed_ids):
                detail_url = detail_format.format(detail)
                yield Request(
                    url=detail_url,
                    callback=self.save_detail,
                    errback=self.err_parse,
                    meta={
                        "page": page,
                        "name": name,
                    })
                self.logger1.info("page {} yield detail {}".format(page, name))
            next_page = re.search(r"page\(\'(\d+)\'\)", "".join(
                response.xpath('//a[contains(., "下一页")]/@onclick')
                .extract())).group(1)
            if not next_page:
                self.logger1.warning(
                    "no more next page, the last page is {}".format(page))
                return
            self.form_data["pageNo"] = "{}".format(next_page)
            yield FormRequest(
                url=response.url,
                dont_filter=True,
                formdata=self.form_data,
                callback=self.parse,
                errback=self.err_parse,
                meta={
                    "page": next_page,
                    "detail_format": detail_format
                })
            self.logger1.info("yield turn page {}".format(next_page))
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
                self.logger1.info("page {} name {} save to ssdb".format(
                    page, name))
            else:
                self.logger1.warning("page {} name {} save failed".format(
                    page, name))
        except Exception as err:
            err_msg = traceback.format_exc()
            self.logger1.warning(
                "failed to save, url {url} error:{err_msg}".format(
                    url=response.url, err_msg=err_msg))

    def err_parse(self, failure):
        self.logger1.warning('failed request page: {}'.format(
            failure.request.url))
