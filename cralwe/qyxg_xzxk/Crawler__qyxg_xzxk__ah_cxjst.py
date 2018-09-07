# -*- coding: utf-8 -*-

"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__ah_cxjst.py
    Description:    行政许可 - 安徽省住房和城乡建设厅
    Author:         hyy
    Date:           2017-11-21
    version:        v.1.0
-------------------------------------------------
"""

import copy
import json
import math
import traceback

import requests
from scrapy import Request
from scrapy.selector.unified import Selector

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll


class Crawler__qyxg_xzxk__ah_cxjst(SpiderAll):
    """
    行政许可 - 安徽省住房和城乡建设厅
    """
    name = 'Crawler__qyxg_xzxk__ah_cxjst'

    def custom_init(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.start_urls = ['http://www.ahjst.gov.cn/ahzjt_Front/Template/Default/double-publicity-open.html']
        self.token_url = 'http://www.ahjst.gov.cn/ahzjt_Front/InfoService/Information.asmx/GetToken'
        self.list_url = "http://www.ahjst.gov.cn/ahzjt_Front/Infoservice/Information.asmx/GetInfoListExtendXK"
        self.detail_url = "http://www.ahjst.gov.cn/ahzjt_Front/Infoservice/Information.asmx/GetDetailXK"
        self.header = {
            "Host": "www.ahjst.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Content-Length": "0"
        }

        self.data = {"Token": '', "PageIndex": "1", "PageSize": "10",
                     "CatgoryNum": "014012", "Name1": "", "Name2": ""}

    def parse(self, response):
        token = json.loads(requests.post(self.token_url, headers=self.header).text, strict=False).get('d', '')
        data = copy.deepcopy(self.data)
        data.update({'Token': token})
        list_content = json.loads(requests.post(self.list_url, headers=self.header, json=data).text,
                                  strict=False).get('d', '')
        cont_list = json.loads(list_content).get('Table', [])
        page_count = math.ceil(int(cont_list[0].get('total', 0)) / 10)
        for page in range(1, page_count + 1):
            yield Request(response.url, callback=self.detail_parse, meta={'page': page}, dont_filter=True)

    def detail_parse(self, response):
        page = response.meta['page']
        token = json.loads(requests.post(self.token_url, headers=self.header).text, strict=False).get('d', '')
        data = copy.deepcopy(self.data)
        data.update({'Token': token, 'PageIndex': str(page)})
        list_content = json.loads(requests.post(self.list_url, headers=self.header, json=data).text,
                                  strict=False).get('d', '')
        cont_list = json.loads(list_content).get('Table', [])
        for cont in cont_list:
            result_dict = {}
            info_id = cont.get('InfoID', '')
            post_data = {"Token": json.loads(requests.post(self.token_url, headers=self.header).text,
                                             strict=False).get('d', ''),
                         "PageIndex": "1", "PageSize": "1", "InfoID": info_id}
            detail_content = json.loads(requests.post(self.detail_url, headers=self.header,
                                                      json=post_data).text, strict=False).get('d', '')
            detail = json.loads(detail_content, strict=False).get('Table', [])[0]

            result_dict['license_code'] = detail.get('name1', '')
            result_dict['case_name'] = detail.get('name2', '')
            result_dict['approval_category'] = detail.get('name3', '')
            result_dict['license_content'] = detail.get('name4', '')
            result_dict['company_name'] = detail.get('name5', '')
            result_dict['credit_code'] = detail.get('name6', '')
            result_dict['organization_code'] = detail.get('name7', '')
            result_dict['regno'] = detail.get('name8', '')
            result_dict['tax_code'] = detail.get('name9', '')
            result_dict['id_number'] = detail.get('name10', '')
            result_dict['frname'] = detail.get('name11', '')
            result_dict['license_start_date'] = detail.get('name12', '')
            result_dict['license_end_date'] = detail.get('name13', '')
            result_dict['license_org'] = detail.get('name14', '')
            result_dict['update'] = detail.get('infodate', '')
            for key, value in result_dict.items():
                result_dict[key] = ''.join(Selector(text=value).xpath('//p//text()').extract()).strip()\
                    if '<p style' in value else value
            yield self.handle_result(response, result_dict, info_id)

    def handle_result(self, response, result_dict, info_id):
        item = self.result_item_assembler(response)
        item['_parsed_data'] = result_dict
        item['bbd_html'] = ''
        item['bbd_url'] = response.url + '?CategoryNum=014012&InfoID={}'.format(info_id)
        item['_id'] = calc_str_md5(info_id)
        return item

    def error_back(self, failure):
        self.logger1.error("failed to get content: {}, try again".format(traceback.format_exc()))
