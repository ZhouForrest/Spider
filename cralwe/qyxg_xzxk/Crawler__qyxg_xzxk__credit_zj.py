# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_zj.py
    Description:    信用浙江-行政许可
    Author:         crazy_jacky
    Date:           2018-01-09
    version:        v.1.0
-------------------------------------------------
"""
from .CreditZhejiang import CreditZhejiang


class Crawler__qyxg_xzxk__credit_zj(CreditZhejiang):
    name = 'Crawler__qyxg_xzxk__credit_zj'
    start_urls = ['http://www.zjcredit.gov.cn/sgs/sgsList01.do?xk_startdate=2015-07-01']

