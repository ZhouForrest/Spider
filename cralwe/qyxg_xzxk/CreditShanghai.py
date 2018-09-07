# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditShanghai.py
    Description:    信用上海
    Author:         hyy
    Date:           2018-01-09
    version:        v.1.0
-------------------------------------------------
"""
import json
import traceback

from scrapy.http.request import Request

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll


class CreditShanghai(SpiderAll):
    """
    Credit shang hai info base class.
    """
    name = 'CreditShanghai'

    def parse(self, response):
        try:
            content = json.loads(response.body.decode())
            page_count = content.get('total', 1)
            for page in range(1, page_count + 1):
                url = self.page_url.format(page)
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
            content_list = json.loads(response.body.decode()).get('gridModel', '')
            for content in content_list:
                if 'xklist' in response.url:
                    detail_id = content.get('xkid', '')
                else:
                    detail_id = content.get('cfid', '')
                detail_url = self.detail_url.format(detail_id)
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
            detail = json.loads(response.body.decode())[0]
            if detail:
                result = {}
                if 'xkid=' in response.url:
                    result['license_code'] = detail.get('xkwsh', '')
                    result['case_name'] = detail.get('xmmc', '')
                    result['approval_category'] = detail.get('splb', '')
                    result['license_content'] = detail.get('xknr', '')
                    result['company_name'] = detail.get('xzxdr', '')
                    result['license_start_date'] = detail.get('xkjdrq', '').replace('/', '-') + ' 00:00:00'
                    result['license_end_date'] = detail.get('xkjzrq', '').replace('/', '-') + ' 00:00:00'
                    result['license_org'] = detail.get('xkjg', '')
                else:
                    result['punish_code'] = detail.get('cfwsh', '')
                    result['case_name'] = detail.get('cfmc', '')
                    result['punish_category_one'] = detail.get('cflb', '')
                    result['punish_type'] = detail.get('cfsy', '')
                    result['punish_basis'] = detail.get('cfyj', '')
                    result['company_name'] = detail.get('xzxdr', '')
                    result['public_date'] = detail.get('cfjdrq', '').replace('/', '-') + ' 00:00:00'
                    result['punish_org'] = detail.get('cfjguan', '')
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
