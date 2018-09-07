# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditGanSuSearch.py
    Description:    信用甘肃 - 行政许可&行政处罚 搜索版
    Author:         QL
    Date:           2018-01-10
    Version:        v.1.0
-------------------------------------------------
"""

import re
import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.commons.utils.selector_util import convert_formal_date
from hive_framework_milk.commons.utils.tools import calc_str_md5, gen_rowkey
from hive_framework_milk.scrapy_spiders.item.parsed_item import ParsedItem
from hive_framework_milk.scrapy_spiders.spiders.spider_seed import Spider_Seed
from .field_mapping import map_field


class CreditGanSuSearch(Spider_Seed):
    name = "CreditGanSuSearch"
    seed_key = None
    search_url_4_legal = None
    search_url_4_person = None

    specific_settings = {
        'ITEM_PIPELINES': {
             'hive_framework_milk.scrapy_spiders.pipeline.result_pipeline.ResultPipeline': 300
        },
    }

    def custom_init(self, *args, **kwargs):
        super().custom_init(*args, **kwargs)
        assert all([self.seed_key, self.search_url_4_legal, self.search_url_4_person]), \
            'please make sure seed_key,search_url_4_legal,search_url_4_person are not empty!'

    def make_request_from_seed(self, data):
        """
        根据种子，产生请求
        :param data:
        :return:
        """
        if isinstance(data, bytes):
            data = data.decode()
        self.logger1.info("Start to search by {}".format(data))
        form_data = {'keyword': data}
        return [
            FormRequest(self.search_url_4_legal, callback=self.parse_list, formdata=form_data,
                        dont_filter=True, meta={'keyword': data, 'type': '法人'}),
            FormRequest(self.search_url_4_person, callback=self.parse_list, formdata=form_data,
                        dont_filter=True, meta={'keyword': data, 'type': '自然人'})
        ]

    def parse_list(self, response):
        """
        Parse the list pages: get the pubdate and target url.
        :param response:
        :return:
        """
        try:
            urls_list = response.xpath('//div[@class="company-messages"]//a/@href').extract()
            if not urls_list:
                self.logger1.info('the result what searching for keyword[{}] in {} is empty!'
                                  .format(response.meta['keyword'], response.meta['type']))
            else:
                for url in set(urls_list):
                    url = response.urljoin(url.strip())
                    yield Request(url, callback=self.parse_detail, errback=self.err_parse_detail)
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
            keys = response.xpath('//p[@class="tab1-p-left"]/text()').extract()
            assert keys, "this page has changed, please check xpath: {]".format(response.url)
            keys = [re.sub(r':|：', '', key) for key in keys]
            values = response.xpath('//p[@class="tab1-p-right"]').xpath('string()').extract()
            result_dict = dict(zip(keys, values))
            for key, value in result_dict.items():
                if key.endswith(('期', '戳')):
                    # 许可生效期、许可截止期、公示日期 等等
                    _, value = convert_formal_date(value, need_time=True)
                    if len(value) == 10:
                        value += ' 00:00:00'
                    result_dict[key] = value

            # 如果没有抓到有效的数据，则重新请求该详情页，至多10次
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

    def handle_result(self, response, result_dict):
        result_dict = map_field(result_dict)
        if 'xzcf' in self.name and 'license_status' in result_dict:
            result_dict['punish_status'] = result_dict.pop('license_status', '')

        item = ParsedItem()
        self.common_item_assembler(response, item)
        item['_parsed_data'] = result_dict
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_params'] = ''
        item['bbd_type'] = self.name.split('__')[-1][:-7]
        item['rowkey'] = gen_rowkey(item, keys=('do_time', 'bbd_type'))
        return item

    def err_parse_list(self, failure):
        self.logger1.error("failed to get list-page's results: {}".format(failure.request.url))

    def err_parse_detail(self, failure):
        self.logger1.warning('failed to request detail page: {}'.format(failure.request.url))
