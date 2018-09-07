# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_ah.py
    Description:    信用安徽-行政许可
    Author:         hyy
    Date:           2017-12-28
    version:        v.1.0
-------------------------------------------------
"""
from .CreditAnhui import CreditAnhui


class Crawler__qyxg_xzxk__credit_ah(CreditAnhui):
    name = 'Crawler__qyxg_xzxk__credit_ah'
    start_urls = ['http://www.creditah.gov.cn/api/doublePublicity/page.jspx?type=1']
    data_status = 'license_status'

