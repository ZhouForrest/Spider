#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__yb_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__yb_l_tax(SC_l_tax_base):
    """宜宾"""
    
    def _line_content_handler(self, lines):
        lines = [re.sub('\s+', ' ', l).strip() for l in lines if re.sub('\s', '', l)]
        _line = []
        for l in lines:
            punish_type_re_result = re.match('.*(处罚事由\s*其他违法[:：].*)', l)
            if punish_type_re_result:
                l = l.replace(' ', ':', 1)
            _line.append(l)
        return _line