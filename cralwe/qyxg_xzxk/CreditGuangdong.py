# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditGuangdong.py
    Description:    信用广东
    Author:         Jack Deng
    Date:           2017-12-19
    Version:        v.1.0
    Lastmodified:   2017-12-20 by Jack Deng
    LastModified:   2018-02-24  by  Jack Deng 双公示行政处罚　bugfix 修改"license_status" 为　"punish_status"
-------------------------------------------------
"""

import datetime
import math
import re
import time
import traceback
import uuid

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditGuangdong(SpiderAll):
    """
    信用广东 crawl base class
    """

    name = "CreditGuangdong"
    specific_settings = {
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'hive_framework_milk.scrapy_spiders.middleware.filterkeywordsmiddleware.FilterKeywordsMiddleware': 300
        },
    }

    filter_keywords_for_page = {
        'http://www.gdcredit.gov.cn/infoTypeAction!getTwoPublicdetail\.do\?id=.*&type=\d+': {
            'key_word_xpath': '//text()',
            'pass_key_word': ['Unknown Host', '错误，访问被禁止', '您因为共享终端被禁止访问网络', ''],
        },
    }
    per_page_num = 100
    post_url = "http://www.gdcredit.gov.cn/infoTypeAction!xzTwoPublicList.do"
    map_type = {
        "3": "行政许可",
        "7": "行政处罚"
    }
    form_data = {
        "type": "",
        "keyWord": "",
        "depId": "",
        "depType": "0",
        "page": "",
        "pageSize": "{}".format(per_page_num)
    }

    def parse(self, response):
        try:
            data_num = int(''.join(response.xpath('//input[@type="hidden" and @id="total"]/@value').extract()))
            page_num = int(math.ceil(data_num / self.per_page_num))
            which_type = re.search(r'.*type=(\d+)', response.url).group(1)
            self.crawl_type = self.map_type.get(which_type, "")
            self.form_data["type"] = which_type
            for page in range(1, page_num + 1):
                self.form_data["page"] = "{}".format(page)
                yield FormRequest(
                    url=self.post_url,
                    dont_filter=True,
                    formdata=self.form_data,
                    callback=self.parse_list,
                    errback=self.err_parse,
                    meta={"page": page}
                )
                self.logger1.info("{} yield turn page {}".format(
                    self.crawl_type, page
                ))
        except:
            err_msg = traceback.format_exc()
            self.logger1.error("Exception on first page {url}, error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_list(self, response):
        try:
            page = response.meta.get("page", 1)
            self.logger1.info("Start to parse list page {} ,each page has {} data".format(
                page, self.per_page_num
            ))
            titles = [til.strip() for til in response.xpath("//table//tr//a/text()").extract()]
            hrefs = [href.strip() for href in response.xpath("//table//tr//a/@href").extract()]
            for title, href in zip(titles, hrefs):
                url = response.urljoin(href)
                yield Request(
                    url=url,
                    callback=self.parse_detail,
                    errback=self.err_parse,
                    meta={"page": page}
                )
                self.logger1.info("{} page {} yield detail {}".format(
                    self.crawl_type, page, title
                ))
        except:
            err_msg = traceback.format_exc()
            self.logger1.error("Exception on list page {url}, error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        try:
            page = response.meta['page']
            title_tds = response.xpath('//div[contains(@class, "content")]/table//tr//td[@class="label"]')
            sec_title_tds = response.xpath('//div[contains(@class, "content")]/table//tr[@class="label"]//td')
            value_tds = response.xpath('//div[contains(@class, "content")]/table//tr//td[@class="value"]')
            sec_value_tds = response.xpath('//div[contains(@class, "content")]/table//tr[@class="value"]//td')
            titles = [clean_all_space(td.xpath('string(.)').extract()).replace(":", "").replace("：", "") for td in title_tds if "相对人代码" not in ''.join(td.xpath('string(.)').extract())]
            sec_titles = [clean_all_space(td.xpath('string(.)').extract()) for td in sec_title_tds]
            values = [clean_all_space(td.xpath('string(.)').extract()) for td in value_tds]
            sec_values = [clean_all_space(td.xpath('string(.)').extract()) for td in sec_value_tds]
            if len(titles) != len(values):
                raise Exception("the length of titles and values are not equal")
            if len(sec_titles) != len(sec_values):
                raise Exception("the length of sec_titles and sec_values are not equal")
            tmp_dict = dict(zip(titles, values))
            if not tmp_dict:
                self.logger1.error("url {} err html {} body {} status_code {}".format(
                    response.url, response.text, response.body, response.status
                ))
                return
            tmp_dict.update(dict(zip(sec_titles, sec_values)))
            res_dict = self.convert_time(map_field(tmp_dict))
            if "xzcf" in self.name:
                if "license_status" in res_dict.keys():
                    res_dict["punish_status"] = res_dict.pop("license_status", "")
            item = self.result_item_assembler(response)
            item["bbd_html"] = ""
            item["_id"] = "{}_{}".format(res_dict.get("company_name", ""), uuid.uuid4())
            item["_parsed_data"] = res_dict
            yield item
            self.logger1.info("{} page {} save data {} to mongodb".format(
                self.crawl_type, page, res_dict.get("company_name", "")
            ))
        except:
            err_msg = traceback.format_exc()
            self.logger1.error("Exception on detail page {url}, error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

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

    def err_parse(self, response):
        self.logger1.error('request {} failed'.format(response.request.url))
