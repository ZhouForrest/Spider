# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_tj.py
    Description:    信用天津 - 行政处罚
    Author:         QL
    Date:           2017-12-18
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditTianJin import CreditTianJin


class Crawler__qyxg_xzcf__credit_tj(CreditTianJin):
    name = 'Crawler__qyxg_xzcf__credit_tj'
    start_urls = ['http://sgs.credittj.gov.cn/XycfList.aspx']
    detail_url = 'http://sgs.credittj.gov.cn/XzcfIdx.aspx?pkid={}'
