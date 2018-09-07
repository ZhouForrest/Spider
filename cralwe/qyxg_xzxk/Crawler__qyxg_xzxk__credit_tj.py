# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_tj.py
    Description:    信用天津 - 行政许可
    Author:         QL
    Date:           2017-12-18
    version:        v.1.0
-------------------------------------------------
"""
from .CreditTianJin import CreditTianJin


class Crawler__qyxg_xzxk__credit_tj(CreditTianJin):
    name = 'Crawler__qyxg_xzxk__credit_tj'
    start_urls = ['http://sgs.credittj.gov.cn/XzxkList.aspx']
    detail_url = 'http://sgs.credittj.gov.cn/XzxkIdx.aspx?pkid={}'
