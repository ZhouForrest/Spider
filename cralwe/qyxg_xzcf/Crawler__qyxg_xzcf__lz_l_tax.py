#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__lz_l_tax.py
:Author: caihang@bbdservice.com
:Date: 2018-06-11 11:27
:Version: v.1.0
:Description: 
"""

import re
import copy
import hashlib
from scrapy.http.request import Request

from hive_framework_milk.scrapy_spiders.item import ImageSeedItem
from hive_framework_milk.commons.state import STATE
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from hive_framework_milk.scrapy_spiders.pipeline import SOURCE_SSDB_PIPELINE_CLASS_PATH


class Crawler__qyxg_xzcf__lz_l_tax(SpiderAll):
    """四川省地方税务局-税务行政处罚公告数据 - 泸州"""
    name = 'Crawler__qyxg_xzcf__lz_l_tax'

    specific_settings = {
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES':
            {
                SOURCE_SSDB_PIPELINE_CLASS_PATH: 300,
            },
    }

    key_word_map = {
        '行政处罚决定书文号': 'punish_code',
        '行政处罚决定文书号': 'punish_code',
        '处罚名称': 'case_name',
        '处罚类别': 'punish_category',
        '处罚事由': 'punish_type',
        '处罚依据': 'punish_basis',
        '行政相对人名称': 'company_name',
        '行政相对人代码-1（统一社会信用代码）': 'credit_code', '行政相对人代码/1（统一社会信用代码）': 'credit_code',
        '行政相对人代码-1（社会统一信用代码）': 'credit_code', '行政相对人统一社会信用代码（纳税人识别号）': 'credit_code',
        '行政相对人代码-2（组织机构代码）': 'organization_code', '行政相对人代码/2（组织机构代码）': 'organization_code',
        '行政相对人代码-3（纳税人识别号）': 'tax_code', '行政相对人代码/3（纳税人识别号）': 'tax_code',
        '行政相对人代码-4（居民身份证号）': 'id_number', '行政相对人代码/4（居民身份证号）': 'id_number',
        '法定代表人姓名': 'frname',
        '处罚结果': 'punish_content',
        '处罚决定日期': 'punish_date',
        '处罚机关': 'punish_org',
        '当前状态': 'punish_status',
        '地方编码': 'administrative_code',
        '数据更新时间': 'update',
        '数据更新时间戳': 'update',
        '备注': 'remark',
        '处罚日期': 'punish_date',
        '统一社会信用代码': 'credit_code',
        '统一社会代码': 'credit_code',
        '公示期限': 'public_period',
        '法定代表人': 'frname',
        '统一社会信用代码（纳税人识别码）': ['credit_code', 'tax_code'],
        '统一社会信用代码（居民身份证）': 'credit_code',
        '统一社会信用代码（纳税人识别号）': ['credit_code', 'tax_code']
    }

    start_urls = ['http://lz.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcfgs/']
    next_page_tpl = 'http://lz.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcfgs/index_{}.html'

    def parse(self, response):
        detail_page_list = re.findall('document.write.*?a href="(.*?\.html)">', response.text)
        if detail_page_list and isinstance(detail_page_list, list):
            detail_page_list = list(set(detail_page_list))
            self.logger1.log_more(
                'Current url: {}, detail length:{}'.format(response.request.url, len(detail_page_list)))
            for detail_url in detail_page_list:
                final_detail_url = response.urljoin(detail_url)
                yield Request(url=final_detail_url, callback=self.parse_detail)

        page_info_list = re.findall('setPage\(.*?(\d+),(\d+),(\d+)', response.text)
        if page_info_list:
            page_info_list = page_info_list[0]
            if len(page_info_list) >= 3:
                total_page = int(page_info_list[0])
                cur_page = int(page_info_list[2])
                if cur_page < total_page:
                    next_page_url = self.next_page_tpl.format(cur_page + 1)
                    next_page_url = response.urljoin(next_page_url)
                    yield Request(url=next_page_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        title = response.xpath('string(//h1)').extract_first().strip()
        pubdate_re = re.match('.*(\d{4}-\d{2}-\d{2}).*', response.xpath('string(//div[@class="time"])').extract_first())
        pubdate_str = pubdate_re.groups()[0]
        status, source_item = self.source_item_assembler(response)
        source_dict = dict(source_item)
        source_dict['title'] = title
        source_dict['pubdate'] = pubdate_str
        table = response.xpath('//div[@class="TRS_Editor"]//p')
        if table:
            # parse table
            item = self.parse_table_page(response, title, pubdate_str)
        else:
            item = self.parse_attach_page(response, source_dict)

        if item:
            yield item

    def parse_table_page(self, response, title_str, pubdate_str):
        data = {}
        p_list = response.xpath('//div[@class="TRS_Editor"]//p')
        cur_key = ''
        for p in p_list:
            p_text = ''.join(p.xpath("string(.)").extract()).strip()
            if p_text:
                splited_list = re.split('：|:|\s', p_text)
                _temp_dict = {}

                for v in splited_list:
                    key = self.key_word_map.get(v.strip(), '')
                    if key:
                        cur_key = key
                        if isinstance(key, list):
                            for kn in key:
                                _temp_dict[kn] = ''
                        else:
                            _temp_dict[key] = ''
                    else:
                        if isinstance(cur_key, list):
                            for ck in cur_key:
                                if ck in _temp_dict:
                                    _temp_dict[ck] += v
                        elif cur_key in _temp_dict:
                            _temp_dict[cur_key] += v
                        elif cur_key in data:
                            data[cur_key] += v
                data.update(copy.deepcopy(_temp_dict))

        parsed_data = self.result_item_assembler(response)
        parsed_data['bbd_html'] = ''
        data['title'] = title_str
        data['pubdate'] = pubdate_str
        parsed_data['_parsed_data'] = data
        return parsed_data

    def parse_attach_page(self, response, source_dict):
        attach_href = re.findall('appHTML = .*?a href="(.*?)"', response.text)
        if attach_href:
            attach_href = attach_href[0]
            attach_href = response.urljoin(attach_href)
            attach_title = ''.join(re.findall('appHTML = .*?target.*?>(.*?)<', response.text))
            md = hashlib.md5()
            md.update(attach_title.encode() + attach_href.encode())
            attach_data = {
                'attachment_title': attach_title,
                "attachment_url": attach_href,
                "attachment_id": md.hexdigest(),
                "upload_status": STATE.INITIAL,
                "download_status": STATE.INITIAL,
            }
            source_dict['attachment_list'] = [attach_data]
        else:
            self.logger1.log_more('Attach url parse failed, url:{}'.format(response.request.url), level='warn')
            source_dict['main'] = response.xpath('string(//div[@class="content"]//p)').extract_first().strip()
        source_dict['bbd_html'] = ''
        item = ImageSeedItem()
        item['seed_data'] = {
            'bbd_table': 'attach',
            'bbd_type': 'seed',
            'bbd_url': response.request.url,
            'seed_data': source_dict
        }
        return item