# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditSichuan.py
    Description:    信用四川
    Author:         hyy
    Date:           2017-12-25
    version:        v.1.0
-------------------------------------------------
"""
import re
import traceback

from scrapy.http.request import Request

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditSichuan(SpiderAll):
    """
    Credit fu jian info base class.
    """
    name = 'CreditSichuan'

    def parse(self, response):
        try:
            page_count = int(''.join(response.xpath("//input[@name='ttPage']/@value").extract()).strip())
            for page in range(1, page_count + 1):
                url = response.url + "&pageNum={}".format(page)
                yield Request(url, callback=self.parse_link, errback=self.error_parse, dont_filter=True)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_link(self, response):
        """
        parse detail page link
        :param response:
        :return:
        """
        try:
            self.logger1.info("Start to parse the detail link of {}".format(response.url))
            link_list = response.xpath("//tr[@align='center']/td[2]/a/@href").extract()
            for link in link_list:
                detail_url = response.urljoin(link.strip())
                yield Request(detail_url, callback=self.parse_detail, errback=self.error_parse,
                              priority=6, meta={'count': 0})
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on parse the link page[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        """
        parse detail page
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse {}'.format(response.url))
            li_list = response.xpath("//div[@class='warp']//li")
            if li_list:
                data_dict = {}
                result = {}
                for li in li_list:
                    title = ''.join(li.xpath("./text()").extract()).strip()[:-1]
                    value = ''.join(li.xpath(".//span").xpath("string()").extract()).strip()
                    if title in ['处罚类别', '处罚类型']:
                        if '处罚类别1' in data_dict.keys():
                            title = '处罚类别2'
                        else:
                            title = '处罚类别1'
                    data_dict.update({title: value})

                result.update(map_field(data_dict))
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
                                  priority=6, meta={'count': count})
                else:
                    self.logger1.info('The page has no content,discard!  {}'.format(response.url))
        except Exception as e:
            self.logger1.warning("Exception on save detail page {} {} {}".format(
                response.url, traceback.format_exc(), e))

    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
