#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__abz_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__abz_l_tax(SC_l_tax_base):
    """阿坝州"""
    
    def parse_table(self, table, data, source):
        find_header = False
        remark_idx = -1
        for tr in table.xpath('.//tr'):
            tds = tr.xpath('.//td')
            if len(tds) in [4]:
                if not find_header:
                    header = [re.sub('\s', '', c) for c in tds.xpath('string(.)').extract()]
                    if '备注' in header:
                        remark_idx = header.index('备注')
                        find_header = True
                key = re.sub('\s', '', ''.join(tds[1].xpath('string(.)').extract()))
                value = re.sub('\s', '', ''.join(tds[remark_idx].xpath('string(.)').extract()))
                if key not in self.key_word_map:
                    self.logger.log_more('key missing {}'.format(key), level='warn')
                else:
                    data[self.key_word_map[key]] = value
            else:
                self.logger.log_more('table template not supported {}'.format(source.get('bbd_url')), level='error')