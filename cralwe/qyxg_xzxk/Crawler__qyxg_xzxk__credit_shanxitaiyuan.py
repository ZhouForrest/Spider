# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_shanxitaiyuan.py
    Description:    信用山西-行政许可
    Author:         hyy
    Date:           2018-01-02
    version:        v.1.0
-------------------------------------------------
"""
from .CreditShanxiTaiyuan import CreditShanxiTaiyuan


class Crawler__qyxg_xzxk__credit_shanxitaiyuan(CreditShanxiTaiyuan):
    name = 'Crawler__qyxg_xzxk__credit_shanxitaiyuan'
    start_urls = ['http://www.creditsx.gov.cn/xzxkPList.jspx?pageNo=1',
                  'http://www.creditsx.gov.cn/xzxkList.jspx?pageNo=1']
