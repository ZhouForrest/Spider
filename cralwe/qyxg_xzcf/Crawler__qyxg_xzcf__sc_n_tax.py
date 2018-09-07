#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__sc_n_tax.py
:Author: caihang@bbdservice.com
:Date: 2018-05-21 14:07
:Version: v.1.0
:Description: 
"""

import re
import uuid
import hashlib
import traceback

from hive_framework_milk.commons.state import STATE
from scrapy.http.request import Request
from hive_framework_milk.scrapy_spiders.item import ParsedItem
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_framework_milk.scrapy_spiders.spiders.spider import Spider
from hive_framework_milk.scrapy_spiders.item.image_seed_item import ImageSeedItem
from hive_framework_milk.scrapy_spiders.pipeline.pipeline_const import RESULT_PIPELINE_CLASS_PATH, SOURCE_SSDB_PIPELINE_CLASS_PATH

class Crawler__qyxg_xzcf__sc_n_tax(Spider):
    """
    四川省国家税务局网-税务行政处罚公告数据
    """
    name = 'Crawler__qyxg_xzcf__sc_n_tax'

    start_urls = ['http://www.sc-n-tax.gov.cn/TaxWeb//wz/zfxxgk/search_list.jsp?site_id=37&id=null&'
                  'site_id=null&item_id=157799&syh=null&xxname=null']

    specific_settings = {'COOKIES_ENABLED': True, 'ITEM_PIPELINES': {
            RESULT_PIPELINE_CLASS_PATH: 300
        }}

    def parse(self, response):
        """
        parse home page and generate detail page href
        """
        try:
            href_list = response.xpath("//a[@title='税务行政处罚公示']/@href").extract()

            id_list = [''.join(re.findall('.*&id=(\d+)', x)) for x in href_list]

            detail_page_base_url = 'http://www.sc-n-tax.gov.cn/TaxWeb//wz/zfxxgktext.jsp?id={}&' \
                                   'site_id=null&item_id=null'

            for _id in id_list:
                detail_page_url = detail_page_base_url.format(_id)
                yield Request(detail_page_url, callback=self.parse_detail_page, errback=self.err_parse)

            # turn page
            page_href_list = response.xpath("//div[@class='page']/a/@href").extract()
            page_text_list = response.xpath("//div[@class='page']/a/text()").extract()
            _page_index = -1
            for index, page_text in enumerate(page_text_list):
                if "下一页" == page_text.strip():
                    _page_index = index
                    break

            if _page_index >= 0:
                next_page_href = response.urljoin(page_href_list[_page_index])
                yield Request(next_page_href, callback=self.parse,
                              errback=self.err_parse, dont_filter=True)

        except Exception:
            err_msg = traceback.format_exc()
            self.logger1.error("parse error, url {}, error message:{}".format(response.url, err_msg))

    def parse_detail_page(self, response):
        """
        parse detail page to get base info and attach file info
        """
        try:
            res = {}
            base_info = self._parse_base_info(response)
            res.update(base_info)

            attachment_data_list = self._parse_attachment_info(response)

            yield self._save_item(response, res, attachment_data_list)
        except Exception:
            err_msg = traceback.format_exc()
            self.logger1.warning("parse detail page error, url {}, error message {}".format(response.url, err_msg))

    def _parse_base_info(self, response):
        from_info = ''.join(response.xpath("//div[@class='from']//text()").extract()).strip()
        organ_name = ''.join(re.findall('信息来源：(.*?)\s', from_info)).strip()
        pubdate = ''.join(re.findall('更新时间：(.*)', from_info)).strip()
        return {'organ_name': organ_name, 'pubdate': pubdate}

    def _parse_attachment_info(self, response):
        attachment_data_list = []
        attachment_href_list = response.xpath("//div[@class='detail']/p/a/@href").extract()
        attachment_title_list = response.xpath("//div[@class='detail']/p/a/text()").extract()

        for index, attachment_href in enumerate(attachment_href_list):
            attachment_href = response.urljoin(attachment_href)
            attachment_title = attachment_title_list[index]
            md = hashlib.md5()
            md.update(attachment_title.encode() + attachment_href.encode())
            attachment_data = {
                "attachment_title": attachment_title,
                "attachment_url": attachment_href,
                "attachment_id": md.hexdigest(),
                "upload_status": STATE.INITIAL,
                "download_status": STATE.INITIAL,
            }
            attachment_data_list.append(attachment_data)
        return attachment_data_list

    def _save_item(self, response, res, attachment_data_list):
        if attachment_data_list:
            return self._save_attach_item(response, res, attachment_data_list)
        else:
            return self._save_parsed_item(response, res)

    def _save_attach_item(self, response, res, attachment_data_list):
        status, item = self.source_item_assembler(response)
        item['bbd_html'] = ''
        res.update(dict(item))
        res.update({
            'bbd_source': '四川省国家税务局网',
            'attachment_list': attachment_data_list
        })

        item['seed_data'] = res
        item['bbd_table'] = 'attach'
        item['bbd_type'] = 'seed'
        attach_item = ImageSeedItem()
        attach_item['seed_data'] = dict(item)
        return attach_item

    def _save_parsed_item(self, response, res):
        result_item = ParsedItem()
        self.common_item_assembler(response, result_item)
        result_item["_id"] = "{}".format(uuid.uuid4())
        result_item["bbd_source"] = '四川省国家税务局网'
        result_item["rowkey"] = gen_rowkey(result_item, keys=('do_time', 'bbd_type'))
        result_item["bbd_html"] = ""
        res['attachment_list'] = []
        result_item["_parsed_data"] = res
        return result_item

    def err_parse(self, response):
        self.logger1.warning("parse {} error".format(response.request.url))