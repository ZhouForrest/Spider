#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__gy_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__gy_l_tax(SC_l_tax_base):
    """广元"""
    
    def _get_lines(self, div):
        lines = div.xpath('./p').xpath('string(.)').extract() or div.xpath('.//p').xpath('string(.)').extract()
        
        all_text = re.sub('\s+', ' ', ''.join(div.xpath('.//text()').extract()))
        # specific handling
        # example: http://gy.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcfgs/201803/t20180328_902620.html
        if '地方编码' in all_text:
            find = False
            for l in lines:
                if '地方编码' in l:
                    find = True
            if not find:
                _lines = div.xpath('.//text()').extract()
                for _l in _lines:
                    if '地方编码' in _l:
                        administrative_code_re_result = re.match('.*(地方编码[:：\s*]\s*\d+).*', all_text)
                        if administrative_code_re_result:
                            lines.append(administrative_code_re_result.groups()[0])
                        break
        # end specific handling
        
        # specific handling http://gy.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcfgs/201711/t20171107_830516.html
        
        # if '处罚决定书文号' in all_text:
        #     find = False
        #     for l in lines:
        #         if '处罚决定书文号' in l:
        #             find = True
        #     if not find:
        #
        # # end specific handling
        return lines
