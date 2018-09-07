#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__nc_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__nc_l_tax(SC_l_tax_base):
    """南充"""
    
    def _specific_handle(self, lines):
        # bug id DCTEST-21846
        idx = 0
        for l in lines:
            if re.match('^行政相对人名称\w+\s+.*', l):
                # e.g.  url: http://nc.sc-l-tax.gov.cn/cdssxc/cdrdzt/ndxytxjs/201805/t20180507_926629.html
                # 行政相对人名称顺  庆区博纳商务服务有限公司  -> 行政相对人名称:顺庆区博纳商务服务有限公司
                lines[idx] = l[:len('行政相对人名称')] + ':' + l[len('行政相对人名称'):].replace(' ', '')
            idx += 1
        
        # end bug id DCTEST-21846
        return lines
    
    def _line_content_handler(self, lines):
        
        lines = [re.sub('\s+', ' ', l).strip() for l in lines if re.sub('\s', '', l)]
        # bug id: DCTEST-21847
        lines = [re.sub('处罚类别2：', '', l).strip() for l in lines]
        # end bug id: # bug id: DCTEST-21847
        
        # bug id: DCTEST-21854
        lines = [re.sub('^([A-Za-z_0-9]+?)', '', l).strip() for l in lines]
        # end bug id: DCTEST-21854
        
        lines = self._specific_handle(lines)
        
        return lines
        