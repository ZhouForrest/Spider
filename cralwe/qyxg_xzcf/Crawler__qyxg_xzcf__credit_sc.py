# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_sc.py
    Description:    信用四川-行政处罚
    Author:         hyy
    Date:           2017-12-25
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditSichuan import CreditSichuan


class Crawler__qyxg_xzcf__credit_sc(CreditSichuan):
    name = 'Crawler__qyxg_xzcf__credit_sc'
    start_urls = ['http://www.creditsc.gov.cn/SCMH/doublePublicController/toDoublePublicPage?keyword=']

