# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditBeijingSearch.py
    Description:    双公示-信用北京-基类-搜索
    Author:         Jack Deng
    Date:           2018-02-08
    Version:        v.1.0

    Lastmodified:       2018-02-08  by  Jack Deng
-------------------------------------------------
"""
import copy
import re
import traceback

from scrapy import FormRequest
from scrapy.http.request import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space, convert_formal_date, xpath_extract_text_no_spaces
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_framework_milk.scrapy_spiders.item.parsed_item import ParsedItem
from hive_framework_milk.scrapy_spiders.spiders.spider_seed import Spider_Seed
from .field_mapping import map_field


class CreditBeijingSearch(Spider_Seed):
    """
    双公示-信用北京-基类
    """

    name = "CreditBeijingSearch"

    custom_settings = {
        'ITEM_PIPELINES': {
             'hive_framework_milk.scrapy_spiders.pipeline.result_pipeline.ResultPipeline': 300
        },
    }

    def custom_init(self, *args, **kwargs):
        """
        检查属性，添加种子队列
        :param args:
        :param kwargs:
        :return:
        """
        super().custom_init(*args, **kwargs)
        if not self.seed_key or not self.search_url:
            raise NotImplementedError("seed_key {} or search_url {} not implemented".format(
                self.seed_key, self.search_url
            ))
        self.seed_queue_names = [self.seed_key]

    def make_request_from_seed(self, data):
        """
        根据种子，产生请求
        :param data:
        :return:
        """
        if isinstance(data, bytes):
            data = data.decode()
        search_url = self.search_url
        self.logger1.info("Start search by {}".format(data))
        form_data = copy.deepcopy(self.form_data)
        form_data["qname"] = data
        return FormRequest(
            url=search_url,
            dont_filter=True,
            callback=self.parse,
            formdata=form_data,
            errback=self.error_parse,
            meta={'key': data}
        )

    def parse(self, response):
        key = response.meta.get("key", "")
        self.logger1.info("Parsing company {}".format(key))
        try:
            for req in self.parse_link(response):
                yield req
            page_str = "".join(response.xpath('//div[@class="w_pages"]//a[last()-1]//text()').extract())
            page_count = int(page_str) if page_str else 0
            self.logger1.info("{} has {} page".format(key, page_count))
            if page_count == 0:
                self.logger1.info("当前种子{}搜索结果为空".format(key))
                return
            form_data = copy.deepcopy(self.form_data)
            for page in range(2, page_count + 1):
                form_data.update({"qname": key, "pageNo": "{}".format(page)})
                yield FormRequest(response.url, formdata=form_data, meta={"page": page, "key":key}, callback=self.parse_link,
                                  errback=self.error_parse, dont_filter=True)
                self.logger1.info("{} turn page {}".format(key, page))
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{key}], error:{err_msg}".format(
                key=key, err_msg=err_msg))

    def parse_link(self, response):
        """
        parse detail page link
        :param response:
        :return:
        """
        try:
            page = response.meta.get("page", 1)
            key = response.meta.get("key", "")
            self.logger1.info(
                "Start to parse page {} the detail link of {}".format(page, key))
            link_list = list(set(response.xpath('//table[@id="tableList"]//tr//a/@href').extract()))
            for link in link_list:
                detail_url = response.urljoin(link.strip())
                yield Request(
                    detail_url,
                    callback=self.parse_detail,
                    errback=self.error_parse,
                    meta={"page":page, "key":key}
                )
                self.logger1.info("yield page {} detail url {}".format(page, key))
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on parse the link page[{key}], error:{err_msg}".format(
                key=key, err_msg=err_msg))

    def parse_detail(self, response):
        """
        parse the detail page.
        :param response:
        :return:
        """
        try:
            self.logger1.info("start to parse detail page: {}".format(response.url))
            request_count = response.meta.get('request_count', 1)
            all_trs = response.xpath('//div[@class="gsxq"]//tr')
            assert all_trs, 'this page maybe changed! please check {}'.format(response.url)
            result_dict = {}
            for tr in all_trs:
                if not xpath_extract_text_no_spaces(tr):
                    continue
                key = re.sub(r':|：|\s', r'', ''.join(tr.xpath('./td/b/text()').extract()))
                value = ''.join(tr.xpath('./td/text()').extract()).strip()
                if key.endswith(('期', '时间')):
                    # 许可决定日期、许可截止期、更新时间 等等
                    _, value = convert_formal_date(value, need_time=True)
                    if len(value) == 10:
                        value += ' 00:00:00'
                result_dict[key] = value

            # 如果没有抓到有效的数据，则重新请求该详情页，至多10次
            if not clean_all_space(''.join(result_dict.values())):
                if request_count < 10:
                    self.logger1.warning("the parsed data was empty, so request again!")
                    yield Request(response.url, callback=self.parse_detail, errback=self.error_parse,
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
        item = ParsedItem()
        self.common_item_assembler(response, item)
        item['_parsed_data'] = map_field(result_dict)
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_type'] = "credit_bj"
        item['rowkey'] = gen_rowkey(item, keys=('do_time', 'bbd_type'))
        item['bbd_params'] = ''
        return item


    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
