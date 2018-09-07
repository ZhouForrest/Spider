# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditShanxiTaiyuan.py
    Description:    信用山西
    Author:         hyy
    Date:           2018-01-02
    Version:        v.1.0
    LastModified:   2018-02-24  by  Jack Deng 双公示行政处罚　bugfix 修改"license_status" 为　"punish_status"
-------------------------------------------------
"""
import re
import traceback

from scrapy.http.request import Request

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditShanxiTaiyuan(SpiderAll):
    """
    Credit shan xi info base class.
    """
    name = 'CreditShanxiTaiyuan'

    def parse(self, response):
        try:
            link_list = response.xpath("//td[@class='t_c']/a/@href").extract()
            if link_list:
                for link in link_list:
                    detail_url = response.urljoin(link.strip())
                    yield Request(detail_url, callback=self.parse_detail, errback=self.error_parse)
                next_page = int(response.url.split("=")[1]) + 1
                url = response.url.split("=")[0] + "={}".format(next_page)
                yield Request(url, callback=self.parse, errback=self.error_parse, dont_filter=True)
            else:
                self.logger1.warning("This page has no data: {}".format(response.url))
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        """
        parse detail page
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse {}'.format(response.url))
            tr_list = response.xpath("//tr")
            if tr_list:
                data_dict = {}
                result = {}
                for tr in tr_list:
                    title = ''.join(tr.xpath(".//th//text()").extract()).strip()[:-1].strip()
                    value = ''.join(tr.xpath(".//td").xpath("string()").extract()).strip()
                    if title in ['处罚类别', '处罚类型']:
                        if '处罚类别1' in data_dict.keys():
                            title = '处罚类别2'
                        else:
                            title = '处罚类别1'
                    data_dict.update({title: value})

                result.update(map_field(data_dict))
                if "xzcf" in self.name:
                    if "license_status" in result.keys():
                        result["punish_status"] = result.pop("license_status", "")
                for key, value in result.items():
                    if 'date' in key:
                        if value.strip().isdigit():
                            val = '{}-{}-{} 00:00:00'.format(value[:4], value[4:6], value[6:])
                        elif ':' in value:
                            val = '-'.join(re.findall(r'(\d+)', value.split(' ')[0])) + ' {}'.format(value.split(' ')[1])
                        else:
                            val = '-'.join(re.findall(r'(\d+)', value)) + ' 00:00:00' if value else ''
                        result[key] = val
                item = self.result_item_assembler(response)
                item['_id'] = calc_str_md5(response.url)
                item['bbd_html'] = ''
                item['_parsed_data'] = result
                yield item
                self.logger1.info('{} save successfully'.format(response.url))
            else:
                count = response.meta['count'] + 1
                if count < 10:
                    self.logger1.info('The page has no content,try!  {}'.format(response.url))
                    yield Request(response.url, callback=self.parse_detail, errback=self.error_parse,
                                  priority=999, meta={'count': count})
                else:
                    self.logger1.info('The page has no content,discard!  {}'.format(response.url))
        except Exception as e:
            self.logger1.warning("Exception on save detail page {} {} {}".format(
                response.url, traceback.format_exc(), e))

    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
