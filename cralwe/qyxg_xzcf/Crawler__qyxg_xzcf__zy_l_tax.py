#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__zy_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-26 9:39
:Version: v.1.0
:Description: 
"""
import re
import hashlib
from datetime import datetime

from hive_framework_milk.commons.state import STATE
from hive_framework_milk.scrapy_spiders.item import ImageSeedItem

from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzcf.Crawler__qyxg_xzcf__dz_l_tax import Crawler__qyxg_xzcf__dz_l_tax


class Crawler__qyxg_xzcf__zy_l_tax(Crawler__qyxg_xzcf__dz_l_tax):
    """四川省地方税务局-税务行政处罚公告数据 - 资阳"""
    name = 'Crawler__qyxg_xzcf__zy_l_tax'
    
    start_urls = ['http://zy.sc-l-tax.gov.cn/cdzwgk/xzgs/xzcfgs/index.html']
    
    next_page_tpl = 'http://zy.sc-l-tax.gov.cn/cdzwgk/xzgs/xzcfgs/index_{}.html'

    key_word_map = {
        '税务处罚决定文书号': 'punish_code',  # gy, 0613
        '行政处罚决定文书号': 'punish_code',
        '行政处罚决定书文号': 'punish_code',
        '政处罚决定文书号': 'punish_code',
        '行政处罚文书号': 'punish_code',
        '行政处罚决定文号': 'punish_code',
        '行政处罚决定书号': 'punish_code',  # ls, 0613
        '行政处罚决定文书': 'punish_code',  # lsz, 0613
        '行政处罚决定文书号 东地一所': 'punish_code',  # ms, 0613 http://jira.bbdops.com/browse/DCTEST-21900
        '政处罚决定书文号': 'punish_code',  # lsz, 0615
        '税务行政处罚决定书文号': 'punish_code',  # lsz, 0615
    
        '处罚名称': 'case_name',
        '处罚类别': 'punish_category',
        '处罚类别1': 'punish_category',
        '罚款类别': 'punish_category',  # sn 0615
        '罚类别': 'punish_category',
        '税务行政处罚处罚类别': 'punish_category',  # cd, 0014
    
        '处罚事由': 'punish_type',
        '处罚是由': 'punish_type',  # lsz 0613
        '罚款事由': 'punish_type',  # lsz 0613
        '出发事由': 'punish_type',  # sn 0615
        '处罚依据': 'punish_basis',
        '行政相对人名称': 'company_name',
        '行政相对人名': 'company_name',
        '行政行对人名称': 'company_name',  # nc 0614
        '政行对人名称': 'company_name',  # nc 0621
    
        '行政相对人代码-1': 'credit_code',
        '行政相对人代码-1（统一社会信用代码）': 'credit_code',
        '行政相对人代码/1（统一社会信用代码）': 'credit_code',
        '行统一社会信用代码': 'credit_code',
        '统一社会信用代码': 'credit_code',
        '统一社会代码': 'credit_code',
        '行政相对人代码-1（社会统一信用代码）': 'credit_code',
        '行政相对人代码（统一社会信用代码）': 'credit_code',
        '统一社会信用代': 'credit_code',
        '行政相对人代码1（统一社会信用代码）': 'credit_code',
        '社会信用代码': 'credit_code',
        '公司 统一社会信用代码': 'credit_code',  # 0613
        '行政相对人代码_1 (统一社会信用代码)': 'credit_code',  # 0613
        '行政相对人代码': 'credit_code',  # nc 0614
        '行政相对人代码_ 1(统一社会信用代码)': 'credit_code',  # ms, 0619
        '相对人代码': 'credit_code',  # nj, 0620
    
        '行政相对人统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信用代码）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信息代码）': 'credit_code',  # 需要特殊处理，乐山
        '社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理, cd, 0613
        '纳税人识别号（或统一社会信用代码）': 'credit_code',  # 需要特殊处理, SN, 0615
    
        '行政相对人代码-2（组织机构代码）': 'organization_code',
        '行政相对人代码/2（组织机构代码）': 'organization_code',
        '行政相对人代码-2': 'organization_code',
        '组织机构代码': 'organization_code',  # 0613
    
        '行政相对人代码-3': 'tax_code',
        '行政相对人代码-3（纳税人识别号）': 'tax_code',
        '行政相对人代码/3（纳税人识别号）': 'tax_code',
        '统一社会信用代码（纳税人识别码）': 'tax_code',
        '纳税人识别号': 'tax_code',
        '行政相对人代码（纳税人识别号）': 'tax_code',
        '纳税识别码': 'tax_code',  # sn, 0625
    
        '行政相对人代码-4（居民身份证号）': 'id_number',
        '行政相对人代码/4（居民身份证号）': 'id_number',
        '行政相对人代码-4 ': 'id_number',
        '行政相对人代码-4': 'id_number',
        '行政相对人代码4（居民身份证号）': 'id_number',  # cd, 0613
        '居民身份证号': 'id_number',  # lsz, 0619
    
        '法定代表人姓名': 'frname',
        '法定代表人': 'frname',
        '法人代表': 'frname',  # lsz, 0613
        '法定代表人（负责人）': 'frname',  # sn 0613
        '法人代表人': 'frname',  # lsz, 0615
        '处罚结果': 'punish_content',
        '兴处罚决定日期': 'punish_date',
        '处罚决定日期': 'punish_date',
        '处罚日期': 'punish_date',
        '处罚机关': 'punish_org',
        '当前状态': 'punish_status',
        '当权状态': 'punish_status',
        '地方编码': 'administrative_code',
        '数据更新时间': 'update',
        '数据更新时间戳': 'update',
        '数据更新录入日期': 'update',  # cd, 0613
        '公示期限': 'public_period',
        '备注': 'remark',
    }
    
    _result_pop_key_list = ['_request_url', '_method', '_header', '_response_url']
    
    def parse_detail(self, response):
        title = response.xpath('string(//h1)').extract_first().strip()
        pubdate_re = re.match('.*(\d{4}-\d{2}-\d{2}).*', response.xpath('string(//div[@class="time"])').extract_first())
        pubdate_str = pubdate_re.groups()[0]
        status, source_item = self.source_item_assembler(response)
        source_dict = dict(source_item)
        source_dict['title'] = title
        source_dict['pubdate'] = pubdate_str
        attach = re.sub('\s', '', ''.join(response.xpath('//div[@class="p_dis_main"]//script').extract()))
        
        if re.match('.*href.*', attach):
            # parse attach
            item = self.parse_attach_page(response, source_dict)
        else:
            item = self.parse_lines(response, source_dict, pubdate_str)

        if item:
            yield item
            
    def parse_attach_page(self, response, source_dict):
        script_str = re.sub('\s+', '', ''.join(response.xpath('string(//div[@class="p_dis_main"]//script)').extract()))
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
        source_dict['content_html'] = self._get_content_html(response)
        item = ImageSeedItem()
        item['seed_data'] = {
            'bbd_table': 'attach',
            'bbd_type': 'seed',
            'bbd_url': response.request.url,
            'seed_data': source_dict
        }
        return item

    def parse_lines(self, response, source, pubdate_str):
        data = {}
        pub_date_str = response.xpath('string(//div[@class="time"])').extract_first()
        pub_date_re_result = re.match('.*(\d{4}-\d{2}-\d{2}).*', pub_date_str)
        if pub_date_re_result:
            pub_str = pub_date_re_result.groups()[0].replace('-', '/')
            data['pubdate'] = pub_str
        else:
            self.logger.log_more('pub_date parse failed', level='warn')
        title = response.xpath('string(//div/h1[@class="f24 fontWr"])').extract_first()
        if title:
            data['title'] = title.strip()
        else:
            self.logger.log_more('title parse failed', level='warn')
    
        if self._find_content_block(response):
            div = self._find_content_block(response)
            self.parse_line(div, data, source)
        else:
            self.logger.log_more('Template not supported', level='warn')
    
        source.update(data)
        source['bbd_html'] = ''
        self._change_date('update', source)
    
        self._change_date('pubdate', source)
        source['bbd_params'] = ''
        source['content_html'] = self._get_content_html(response)

        parsed_data = self.result_item_assembler(response)
        parsed_data['bbd_html'] = ''
        source['title'] = title
        source['pubdate'] = pubdate_str
        source['content_html'] = self._get_content_html(response)
        self._pop_keys4result(source)
        parsed_data['_parsed_data'] = source
        return parsed_data
    
    def _pop_keys4result(self, source):
        for k in self._result_pop_key_list:
            try:
                source.pop(k, '')
            except:
                pass
        
    
    def _change_date(self, name, source):
        date_str = source.get(name)
        if not isinstance(date_str, str):
            self.logger.log_more('name:{} date_str not support: {}'.format(name, date_str))
            return
        if len(date_str) >= 10:
            date_str = date_str[:10]
        try:
            if '-' in date_str and date_str.count('-') >= 2:
                _date = datetime.strptime(date_str, '%Y-%m-%d')
                _date_str = _date.strftime('%Y/%m/%d')
            elif '/' in date_str and date_str.count('/') >= 2:
                _date = datetime.strptime(date_str, '%Y/%m/%d')
                _date_str = _date.strftime('%Y/%m/%d')
            else:
                self.logger.log_more('name: {}, date_str not support: {}'.format(name, date_str))
                return
            if _date_str:
                source[name] = _date_str
            else:
                self.logger.log_more(
                    '{} change format failed:{}, url:{}'.format(name, source.get(name), source['bbd_url']))
        except:
            pass

    def parse_line(self, div, data, source):
        lines = self._get_lines(div)
        lines = self._line_content_handler(lines)
        lines = self._assemble_lines(lines)
        for l in lines:
            l_split_re = re.match('(.*)[:：](.*)', l)
            if l_split_re:
                if l.count(':') + l.count('：') > 1:
                    if l.find(':') > 0 > l.find('：'):
                        key = l[:l.find(':')]
                        value = l[l.find(':') + 1:]
                    elif l.find(':') > l.find('：') > 0:
                        key = l[:l.find('：')]
                        value = l[l.find('：') + 1:]
                    elif l.find('：') > l.find(':') > 0:
                        key = l[:l.find(':')]
                        value = l[l.find(':') + 1:]
                    elif l.find('：') > 0 > l.find(':'):
                        key = l[:l.find('：')]
                        value = l[l.find('：') + 1:]
                    else:
                        self.logger.log_more('Found key not matched in : :, l: {}'.format(l), level='warn')
                        continue
                else:
                    key = l_split_re.groups()[0].strip()
                    value = l_split_re.groups()[1].strip()
                if key in self.key_word_map:
                    data[self.key_word_map[key]] = value
                    self._data_post_handle(key, value, data)
                else:
                    self.logger.log_more('Found key not matched in re, l:{}, key:{}'.format(l, key), level='warn')
            else:
                if l:
                    # bug id: DCTEST-21801
                    key = l
                    if key in self.key_word_map:
                        data[self.key_word_map[key]] = ''
                        self._data_post_handle(key, '', data)
                    else:
                        # bug id: DCTEST-21841
                        key_split_list = key.split(' ')
                        if key_split_list:
                            if key_split_list[0] in self.key_word_map:
                                value = ''.join(key_split_list[1:]) if len(key_split_list) > 1 else ''
                                data[self.key_word_map[key_split_list[0]]] = value
                                self._data_post_handle(key, value, data)
                            else:
                                self.logger.log_more('Found key not matched in l, l:{}, key:{}'.format(l, key),
                                                     level='warn')
                        else:
                            self._parse_line_with_out_sep(data, l)
                            # end bug id: DCTEST-21841
                            # end bug id: DCTEST-21801
                else:
                    self.logger.log_more('Parse line failed, l:{}: url:{}'.format(l, source.get('bbd_url')),
                                         level='warn')

    def _assemble_lines(self, lines) -> list:
        return lines

    @staticmethod
    def _find_content_block(response):
        return response.xpath('//div[@class="TRS_Editor"]|//div[@class="content"]')

    # @staticmethod
    def _data_post_handle(self, key, value, data):
        if key in ['统一社会信用代码（纳税人识别号）', '纳税人识别号（统一社会信用代码）',
                   '行政相对人统一社会信用代码（纳税人识别号）', '纳税人识别号（统一社会信息代码）',
                   '社会信用代码（纳税人识别号）', '纳税人识别号（或统一社会信用代码）']:
            if data.get('tax_code', None) is None:
                data['tax_code'] = value
        # add lvfeng 0621, for nj,
        # sample: http://sn.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcf/201804/t20180427_921819.html
        if re.search('（统一社会信用代码）|（组织机构代码）|（居民身份证号）|纳税人识别号）|（纳税人识别号）', value):
            self.logger.log_more('Change value from:{}'.format(value))
            value = value.replace('（统一社会信用代码）', '', 1).replace('（组织机构代码）', '', 1).replace('（居民身份证号）', '', 1). \
                replace('纳税人识别号）', '', 1).replace('（纳税人识别号）', '', 1).replace("（", '', 1).replace("）", '', 1).strip()
            try:
                self.logger.log_more('Change value to:{}'.format(value))
                data[self.key_word_map[key]] = value
            except:
                self.logger.log_more('Replace value failed, value: {}'.format(value))
                pass
                # end lvfeng 0621

    def _get_lines(self, div):
        # get lines
        return div.xpath('./p').xpath('string(.)').extract() or div.xpath('.//p').xpath('string(.)').extract()

    def _line_content_handler(self, lines):
        # post handler
        return [re.sub('\s+', ' ', l).strip() for l in lines if re.sub('\s', '', l)]

    def _parse_line_with_out_sep(self, data, l):
        pass

    def _get_content_html(self, response):
        # get content_html,
        # git content with html tags.
        plain_html_str = ''.join(response.xpath('//div[@class="p_dis_main"]').extract()) or \
                         ''.join(response.xpath('.').extract())
        return plain_html_str