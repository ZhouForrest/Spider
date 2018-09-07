#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__dz_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-04 9:57
:Version: v.1.0
:Description: 
"""
import re
import hashlib
from scrapy.http.request import Request

from hive_framework_milk.scrapy_spiders.item import ImageSeedItem
from hive_framework_milk.commons.state import STATE
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from hive_framework_milk.scrapy_spiders.pipeline import SOURCE_SSDB_PIPELINE_CLASS_PATH


class Crawler__qyxg_xzcf__dz_l_tax(SpiderAll):
    """四川省地方税务局-税务行政处罚公告数据 - 达州"""
    name = 'Crawler__qyxg_xzcf__dz_l_tax'

    specific_settings = {
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES':
            {
                SOURCE_SSDB_PIPELINE_CLASS_PATH: 300,
            },
    }

    key_word_map = {
        '行政处罚决定文书号': 'punish_code',
        '行政处罚决定书文号': 'punish_code',
        '政处罚决定文书号': 'punish_code',
        '行政处罚文书号': 'punish_code',
    
        '处罚名称': 'case_name',
        '处罚类别': 'punish_category', '处罚类别1': 'punish_category',
        '罚类别': 'punish_category',
        '处罚事由': 'punish_type',
        '处罚依据': 'punish_basis',
        '行政相对人名称': 'company_name', '行政相对人名': 'company_name',
    
        '行政相对人代码-1': 'credit_code',
        '行政相对人代码-1（统一社会信用代码）': 'credit_code',
        '行政相对人代码/1（统一社会信用代码）': 'credit_code', '行统一社会信用代码': 'credit_code',
        '统一社会信用代码': 'credit_code',
        '统一社会代码': 'credit_code',
        '行政相对人代码-1（社会统一信用代码）': 'credit_code',
        '行政相对人代码（统一社会信用代码）': 'credit_code', '统一社会信用代': 'credit_code', '行政相对人代码1（统一社会信用代码）': 'credit_code',
    
        '行政相对人统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信用代码）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信息代码）': 'credit_code',  # 需要特殊处理，乐山
    
        '行政相对人代码-2（组织机构代码）': 'organization_code',
        '行政相对人代码/2（组织机构代码）': 'organization_code',
        '行政相对人代码-2': 'organization_code',
    
        '行政相对人代码-3': 'tax_code',
        '行政相对人代码-3（纳税人识别号）': 'tax_code',
        '行政相对人代码/3（纳税人识别号）': 'tax_code',
        '统一社会信用代码（纳税人识别码）': 'tax_code',
        '纳税人识别号': 'tax_code',
        '行政相对人代码（纳税人识别号）': 'tax_code',
    
        '行政相对人代码-4（居民身份证号）': 'id_number',
        '行政相对人代码/4（居民身份证号）': 'id_number',
        '行政相对人代码-4 ': 'id_number',
        '行政相对人代码-4': 'id_number',
    
        '法定代表人姓名': 'frname',
        '法定代表人': 'frname',
        '处罚结果': 'punish_content',
        '兴处罚决定日期': 'punish_date',
        '处罚决定日期': 'punish_date', '处罚日期': 'punish_date',
        '处罚机关': 'punish_org',
        '当前状态': 'punish_status',
        '地方编码': 'administrative_code',
        '数据更新时间': 'update',
        '数据更新时间戳': 'update',
        '公示期限': 'public_period',
        '备注': 'remark',
    
    }
    
    start_urls = ['http://dz.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index.html']
    
    next_page_tpl = 'http://dz.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index_{}.html'
    
    def parse(self, response):
        page_script_str = response.xpath('string(//div[@class="p_list_next f14"])').extract_first()
        page_script_str = re.sub('\s+', '', page_script_str)
        total_page_re = re.match('.*page\',(\d+),\d+,(\d+).*', page_script_str)
        if total_page_re:
            total_page = int(total_page_re.groups()[0])
            cur_page = int(total_page_re.groups()[1])
            
            if cur_page < total_page - 1:
                next_page = cur_page + 1
                yield Request(url=self.next_page_tpl.format(next_page), callback=self.parse, dont_filter=True)
        detail_script_str = re.sub('\s+', '', ''.join(response.xpath('//div[@class="contR fr"]//script').extract()))
        detail_page_list = re.findall('(\./\d+/\w+\d+_\d+\.html)', detail_script_str)
        
        if detail_page_list and isinstance(detail_page_list, list):
            detail_page_list = list(set(detail_page_list))
            self.logger1.log_more('Current url: {}, detail length:{}'.format(response.request.url, len(detail_page_list)))
            for detail_url in detail_page_list:
                final_detail_url = response.urljoin(detail_url)
                yield Request(url=final_detail_url, callback=self.parse_detail)
        
    def parse_detail(self, response):
        title = response.xpath('string(//h1)').extract_first().strip()
        pubdate_re = re.match('.*(\d{4}-\d{2}-\d{2}).*', response.xpath('string(//div[@class="time"])').extract_first())
        pubdate_str = pubdate_re.groups()[0]
        status, source_item = self.source_item_assembler(response)
        source_dict = dict(source_item)
        source_dict['title'] = title
        source_dict['pubdate'] = pubdate_str
        table = response.xpath('//div[@class="TRS_Editor"]//table')
        if table:
            # parse table
            item = self.parse_table_page(response, title, pubdate_str)
        else:
            item = self.parse_attach_page(response, source_dict)
        if item:
            yield item
        
    def parse_table_page(self, response, title_str, pubdate_str):
        table = response.xpath('//div[@class="TRS_Editor"]//table')
        find_header = False
        data = {}
        for tr in table.xpath('//tr'):
            if len(tr.xpath('.//td')) < 4:
                self.logger1.log_more('Skip none data')
                continue
            if not find_header:
                find_header = True
                continue
            key = re.sub('\s+', '', ''.join(tr.xpath('.//td')[1].xpath('string(.)').extract()))
            value = re.sub('\s+', '', ''.join(tr.xpath('.//td')[2].xpath('string(.)').extract()))
            if key in self.key_word_map:
                data[self.key_word_map[key]] = value
            else:
                self.logger1.log_more('Map key failed: {}'.format(response.request.url), level='warn')
        parsed_data = self.result_item_assembler(response)
        parsed_data['bbd_html'] = ''
        data['title'] = title_str
        data['pubdate'] = pubdate_str
        parsed_data['_parsed_data'] = data
        return parsed_data
    
    def parse_attach_page(self, response, source_dict):
        script_str = re.sub('\s+', '', ''.join(response.xpath('string(//div[@class="content"]//script)').extract()))
        attach_url_re = re.match('.*href="(\./\w+\..*)"target.*', script_str)
        if attach_url_re:
            attach_url = response.urljoin(attach_url_re.groups()[0])
            attach_title = re.match('.*>(.*\..*)</a.*', script_str).groups()[0]
            md = hashlib.md5()
            md.update(attach_title.encode() + attach_url.encode())
            attach_data = {
                'attachment_title': attach_title,
                "attachment_url": attach_url,
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
        