#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__pzh_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__pzh_l_tax(SC_l_tax_base):
    """攀枝花"""
    def _get_lines(self, div):
        lines = div.xpath('./p').xpath('string(.)').extract() or div.xpath('.//p').xpath('string(.)').extract()
        return [re.sub('[;；]', ':', l, 1) for l in lines]