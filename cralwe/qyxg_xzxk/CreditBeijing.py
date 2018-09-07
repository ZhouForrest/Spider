# -*- coding:utf8 -*-

"""
-------------------------------------------------
    Copyright:      2018, BBD Tech. Co.,Ltd.
    File Name:      CreditBeijing.py
    Description:    信用北京 - 行政许可&行政处罚
    Author:         QL
    Date:           2018-01-09
    Version:        v.1.0
-------------------------------------------------
"""

import copy
import re
import traceback

from scrapy import Request, FormRequest

from hive_framework_milk.commons.utils.selector_util import clean_all_space, xpath_extract_text_no_spaces
from hive_framework_milk.commons.utils.selector_util import convert_formal_date
from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditBeijing(SpiderAll):
    """
    信用北京 - 行政许可&行政处罚
    """
    name = 'CreditBeijing'
    post_url = 'http://cxcj.creditbj.gov.cn/xyData/front/search/list.shtml'

    typeId = ''

    form_data = {
        "typeId": "",
        "regionId": "1",
        "objId": "1",
        "pageNo": "1",
        "qname": "",
        "twoTypeId3": "733",
        "twoTypeId4": "741",
        "twoTypeId5": "18",
        "twoTypeId69": "71",
        "twoTypeId761": "767",
        "regionType": "true",
        "objType": "true",
    }

    def get_ext_requests_or_urls(self):
        url = 'http://cxcj.creditbj.gov.cn/xyData/front/search/initial.shtml?oneTypeId=5'
        self.logger1.info('start to request initial url:{}'.format(url))
        assert self.typeId, 'please make sure typeId is not empty!'
        self.form_data.update({'typeId': self.typeId, "twoTypeId5": self.typeId})
        return FormRequest(self.post_url, callback=self.parse, errback=self.err_parse,
                           formdata=self.form_data, dont_filter=True)

    def parse(self, response):
        """
        get pages and request all the list-pages.
        :param response:
        :return:
        """
        try:
            page = response.meta.get("page", 1)
            self.logger1.info('start to parse page {} url:{}'.format(page, response.url))
            # /xyData/front/search/detail.shtml?typeId=19&catalog=xybj_data_credi_sgs_xzxk&id=1258528
            trs = response.xpath(".//table[@id='tableList']//tr")[1:]
            for tr in trs:
                url = response.urljoin(''.join(tr.xpath(".//a//@href").extract()).strip())
                yield Request(url, callback=self.parse_detail, errback=self.err_parse_detail)

            # 翻页
            next_page_str = ''.join(
                response.xpath(".//div[@class='w_pages']//a[contains(text(), '下一页')]//@onclick").extract())
            page = int(''.join(re.findall("page\((\d+)\)", next_page_str)) or 1)
            if page >= 2:
                formdata = copy.deepcopy(self.form_data)
                formdata.update({"pageNo": str(page)})
                yield FormRequest(self.post_url, callback=self.parse, formdata=formdata, meta={"page": page},
                                  errback=self.err_parse, dont_filter=True)
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
        item = self.result_item_assembler(response)
        item['_parsed_data'] = map_field(result_dict)
        item['_id'] = calc_str_md5(response.url)
        item['bbd_html'] = ''
        item['bbd_params'] = ''
        return item

    def err_parse(self, failure):
        self.logger1.warning('failed to request init page: {}'.format(failure.request.url))

    def err_parse_detail(self, failure):
        self.logger1.warning('failed to request detail page: {}'.format(failure.request.url))
