# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_ah.py
    Description:    信用安徽-行政处罚
    Author:         hyy
    Date:           2017-12-28
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditAnhui import CreditAnhui


class Crawler__qyxg_xzcf__credit_ah(CreditAnhui):
    name = 'Crawler__qyxg_xzcf__credit_ah'
    start_urls = ['http://www.creditah.gov.cn/api/doublePublicity/page.jspx?type=2']
    data_status = 'punish_status'

