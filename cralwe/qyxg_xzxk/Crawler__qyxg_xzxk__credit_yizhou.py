#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzxk__credit_yizhou.py
:Description: 
:Author: liqingqing@bbdservice.com
:Date: 2018-08-06 下午4:52
:Version: v.1.0
"""
import re
import traceback
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider


class Crawler__qyxg_xzxk__credit_yizhou(Spider):
    name = "Crawler__qyxg_xzxk__credit_yizhou"

    urls = [
              "http://www.creditxz.gov.cn/XzCreditWeb/xzxkList.jspx",
              "http://www.creditxz.gov.cn/XzCreditWeb/xzxkPList.jspx"
              ]
    form_data = [
        {
        "sgstype": "",
        "pageNo": "1",
        "totalCount": "60",
        "typename": "lxzxk",
        "istopage": "true",
        "nextpageurl": "/XzCreditWeb/xzxkList.jspx",
        "xkWsh": "",
        "xkXmmc": "",
        "isquery": "true",
        "xkXdr": "",
        "depId": "",
        "xkXzjg": "",
        "startdate": "",
        "enddate": ""
        },
        {
        "pageNo": "1",
        "sgstype": "",
        "xkXdrSfz": "",
        "xkXmmc": "",
        "isquery": "true",
        "xkXdr": "",
        "depId": "",
        "xkXzjg": "",
        "startdate": "",
        "enddate": ""
    }]

    def get_ext_requests_or_urls(self):
        requests = []
        for i in range(len(self.urls)):
            form_data = self.form_data[i]
            request = FormRequest(url=self.urls[i], formdata=form_data, meta={"fd": form_data},
                                  callback=self.parse, errback=self.err_parse, dont_filter=True)
            requests.append(request)
        return requests

    def parse(self, response):
        form_data = response.meta.get("fd", {})
        self.logger1.info("start get pages in parse function, url:{}".format(response.url))
        try:
            page_str = ''.join(response.xpath(".//div[@class='page']//a[last()]//@onclick").extract())
            pages = ''.join(re.findall("(\d+)", page_str))
            pages = int(pages) if pages else 1

            # 翻页
            for page in range(1, pages+1):
                form_data.update({"pageNo": str(page)})
                yield FormRequest(url=response.url, formdata=form_data, callback=self.parse_page,
                                  meta={"pg": page},
                                  errback=self.err_parse, dont_filter=True)
        except Exception:
            msg = traceback.format_exc()
            self.logger1.error("something goes wrong in parse function: {}".format(msg))

    def parse_page(self, response):
        page = response.meta.get("pg", 1)
        self.logger1.info("start get detail list in parse_page function, url: {}, page: {}".format(response.url, page))
        try:
            trs = response.xpath(".//table[@class='table_list']//tr[position() > 1]")
            for tr in trs:
                detail_url = response.urljoin(''.join(tr.xpath(".//a//@href").extract()).strip())
                yield Request(detail_url, callback=self.parse_detail, meta={"pg": page}, errback=self.err_parse)
        except Exception:
            msg = traceback.format_exc()
            self.logger1.error("something goes wrong in parse_page function: {}".format(msg))

    def parse_detail(self, response):
        page = response.meta.get("pg", 1)
        self.logger1.info("start get detail page source, page:{}, url:{}".format(page, response.url))
        try:
            status, item = self.source_item_assembler(response)
            if status:
                yield item
                self.logger1.info("detail has been saved successfully, url:{}".format(response.url))
            else:
                self.logger1.warning("something wrong with detail page, url:{}".format(response.url))
        except Exception:
            msg = traceback.format_exc()
            self.logger1.error("something goes wrong in parse_page function: {}".format(msg))

    def err_parse(self, response):
        self.logger1.error("{} goes wrong...".format(response.request.url))





