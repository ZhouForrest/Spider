#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__sn_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__sn_l_tax(SC_l_tax_base):
    """遂宁"""

    def _get_lines(self, div):
        lines = div.xpath('./p').xpath('string(.)').extract() or div.xpath('.//p').xpath('string(.)').extract()
        mapped_keys = list(self.key_word_map.keys())
        br_newline = False
        
        # handle for example: http://sn.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcf/201805/t20180525_936275.html
        # lines in one p, line split with tag: <br>
        for l in lines:
            duped_keys = set()
            key_in_line_ele_count = 0
            for k in mapped_keys:
                if k in l and self.key_word_map[k] not in duped_keys:
                    key_in_line_ele_count += 1
                    duped_keys.add(self.key_word_map[k])
            if key_in_line_ele_count > 1:
                br_newline = True
                break
        if br_newline:
            lines = div.xpath('.//p/text()').extract()
        # end
        
        # start
        # e.g. 92510921MA65GXL975法定代表人姓名：张谋
        # http://sn.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcf/201806/t20180605_943673.html
        _lines = []
        for l in lines:
            if re.match('\s*([a-zA-Z_0-9]*法定代表人姓名).*', l):
                l = re.sub('[a-zA-Z_0-9]*', '', l.strip())
            _lines.append(l)
        # end
        return _lines
