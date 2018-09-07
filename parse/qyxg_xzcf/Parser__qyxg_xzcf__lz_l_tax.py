#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__lz_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__lz_l_tax(SC_l_tax_base):
    """泸州"""

    def _assemble_lines(self, lines):
        _new_line = []
        tmp_str = ''
        for line in lines:
            if ':' in line or '：' in line:
                _new_line.append(tmp_str)
                tmp_str = line
            else:
                tmp_str += line
        _new_line.append(tmp_str)
        return _new_line