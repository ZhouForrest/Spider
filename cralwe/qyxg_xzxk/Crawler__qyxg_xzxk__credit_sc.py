# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_sc.py
    Description:    信用四川-行政许可
    Author:         hyy
    Date:           2017-12-25
    version:        v.1.0
-------------------------------------------------
"""
from .CreditSichuan import CreditSichuan


class Crawler__qyxg_xzxk__credit_sc(CreditSichuan):
    name = 'Crawler__qyxg_xzxk__credit_sc'
    start_urls = ['http://www.creditsc.gov.cn/SCMH/doublePublicController/toDoublePublicPage2?&keyword=']

