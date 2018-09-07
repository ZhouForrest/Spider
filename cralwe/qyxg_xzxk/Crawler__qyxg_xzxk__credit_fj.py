# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_fj.py
    Description:    信用福建-行政许可
    Author:         hyy
    Date:           2017-12-18
    version:        v.1.0
-------------------------------------------------
"""
from .CreditFujian import CreditFujian


class Crawler__qyxg_xzxk__credit_fj(CreditFujian):
    name = 'Crawler__qyxg_xzxk__credit_fj'
    start_urls = ['http://www.fjcredit.gov.cn/creditsearch.permissionList.phtml?id=&keyword=']

