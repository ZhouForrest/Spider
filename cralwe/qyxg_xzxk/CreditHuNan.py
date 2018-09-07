# -*- coding:utf8 -*-

"""
-------------------------------------------------
    Copyright:      2017, BBD Tech. Co.,Ltd.
    File Name:      CreditHuNan.py
    Description:    信用湖南 - 行政许可&行政处罚
    Author:         QL
    Date:           2017-12-20
    Version:        v.1.0
-------------------------------------------------
"""

import json
import math
import re
import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_strip, xpath_extract_text_no_spaces
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditHuNan(SpiderAll):
    """
    信用湖南 - 行政许可&行政处罚
    """
    name = 'CreditHuNan'

    def parse(self, response):
        """
        get pages and request all the list-pages.
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse initial url:{}'.format(response.url))
            script_text = xpath_extract_text_strip(response, '//script')
            datas = script_text[script_text.find('["'): script_text.find(',]') + 2].replace(',]', ']')
            perPage = int(re.search(r'perPage:\s*(\d+)', script_text).group(1))
            totalRecord = int(re.search(r'totalRecord:\s*(\d+)', script_text).group(1))
            total_pages = int(math.ceil(totalRecord * 1.0 / perPage))
            id2 = re.search(r"id2:\s*'(\w+)'", script_text).group(1)
            proxy_url = re.search(r"proxyUrl:\s*'(.+?)'", script_text).group(1)
            post_url_prefix = response.urljoin(proxy_url)
            detail_url_prefix = response.urljoin(re.search(r"href\s*=\s*'(.+)'\+id", script_text).group(1))

            start = 2
            end = total_pages + 1
            if 'xycs.changsha.gov.cn' in response.url:
                start = 1
            for page in range(start, end):
                startrecord = perPage * (page - 1) + 1
                endrecord = perPage * page if page < total_pages else totalRecord
                url = post_url_prefix + '?startrecord={}&endrecord={}&perpage={}&totalRecord={}' \
                    .format(startrecord, endrecord, perPage, totalRecord)
                meta = {'detail_url_prefix': detail_url_prefix, 'page_num': page}
                yield FormRequest(url, callback=self.parse_list, errback=self.err_parse_list,
                                  formdata={'id2': id2}, dont_filter=True, meta=meta)

            # 发出第一页中的列表URL的请求
            for req in self.req_detail(datas, detail_url_prefix):
                yield req
        except:
            self.logger1.warning('parse list pages wrong: {}'.format(traceback.format_exc()))

    def req_detail(self, datas, detail_url_prefix):
        if not datas:
            return None
        for data in json.loads(datas):
            # 'XK$046A9B72C47073EAC8660AA1AA56AC52670A5$湘乡市湘房房地产开发有限公司$2017-12-22'
            _id = re.search(r'\$(\w+)\$', data).group(1)
            url = detail_url_prefix + _id
            yield Request(url, callback=self.parse_detail, errback=self.err_parse_detail)

    def parse_list(self, response):
        """
        Parse the list pages: get the pubdate and target url.
        :param response:
        :return:
        """
        try:
            page_num = response.meta.get('page_num', 1)
            detail_url_prefix = response.meta['detail_url_prefix']
            self.logger1.info('parse the {} page now'.format(page_num))
            all_text = response.text
            datas = all_text[all_text.find('["'): all_text.find(',]') + 2].replace(',]', ']')
            assert datas, "the web page maybe change in {}, please check".format(response.url)
            for req in self.req_detail(datas, detail_url_prefix):
                yield req
        except:
            self.logger1.warning('parse list pages wrong: {}'.format(traceback.format_exc()))

    def parse_detail(self, response):
        """
        parse the detail page.
        :param response:
        :return:
        """
        try:
            self.logger1.info("start to parse detail page: {}".format(response.url))
            request_count = response.meta.get('request_count', 1)

            # 详情页有两种格式
            if response.xpath('//td[@class="xzcf_jds"]'):
                result_dict = self.parse_data(response, 'td[@class="xzcf_mc"]')
                result_dict['正文'] = xpath_extract_text_strip(response, '//td[@class="xzcf_jds"]')
            else:
                result_dict = self.parse_data(response, 'td[@class="xzcf_tb"]')
                result_dict['正文'] = result_dict.pop('行政处罚决定书（全文或摘要）', '') or result_dict.pop('行政许可决定书（全文或摘要）', '')
            if not clean_all_space(''.join(result_dict.values())):
                if request_count < 10:
                    self.logger1.warning("the parsed data was empty, so request again!")
                    yield Request(response.url, callback=self.parse_detail, errback=self.err_parse_detail,
                                  dont_filter=True, meta={'request_count': request_count + 1})
                else:
                    self.logger1.warning("this page has requested more than 10 times, ignore it!")
            else:
                yield self.handle_result(response, result_dict)
                self.logger1.info("store data to database successfully!")
        except:
            err_msg = traceback.format_exc()
            self.logger.warning("failed to parse detail page, url {url} error:{err_msg}"
                                .format(url=response.url, err_msg=err_msg))

    def parse_data(self, response, key_xpath):
        """
        样例： http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/licenseDetail.do?
                id=C6DAB489F8766C557FD3D782F4EE4FFB82E8BF9088FB5C6446E41FB4CA7EB421
        或者
             http://credit.xiangtan.gov.cn/sgs/webInfo/licenseDetail.do?
                id=046A9B72C47073EAC8660AA1AA56AC540AF35BFB93E469B4
        :param response: 
        :param key_xpath: 
        :return: 
        """
        result_dict = {}
        for tr in response.xpath('//table[@class="xzcf_bg"]//tr'):
            if '法定代表人（或单位负责人）' in xpath_extract_text_no_spaces(tr):
                key1 = re.sub(r':|：', r'', xpath_extract_text_no_spaces(tr, key_xpath))
                key2 = re.sub(r':|：', r'', xpath_extract_text_no_spaces(tr, './/span[@class="xzcf_mc"]'))
                values = ''.join(tr.xpath('td[@class="xzcf_xx"]//text()').extract()).strip()
                value1 = values[:values.find(key2)].strip()
                value2 = values[values.find(key2) + len(key2) + 1:].strip()
                result_dict[key1] = value1
                result_dict[key2] = value2
            else:
                key = re.sub(r':|：', r'', xpath_extract_text_no_spaces(tr, key_xpath))
                value = xpath_extract_text_strip(tr, '(td[@class="xzcf_xx"] | td[@class="xzcf_xx2"])')
                if key.endswith('期'):
                    if value.isdigit() and len(value) == 8:
                        # 样例： '20170618'
                        value = '{}-{}-{} 00:00:00'.format(value[:4], value[4:6], value[6:])
                    elif value:
                        value = '{}-{:0>2}-{:0>2} 00:00:00'.format(*re.findall(r'\d+', value)[:3])
                result_dict[key] = value
        return result_dict

    def handle_result(self, response, result_dict):
        item = self.result_item_assembler(response)
        item['_parsed_data'] = map_field(result_dict)
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_params'] = ''
        return item

    def err_parse_detail(self, failure):
        self.logger1.warning('failed to request detail page: {}'.format(failure.request.url))

    def err_parse_list(self, failure):
        self.logger1.error("failed to get list-page's results: {}".format(failure.request.url))
