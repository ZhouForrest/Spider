# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_shanxitaiyuan.py
    Description:    信用山西-行政处罚
    Author:         hyy
    Date:           2018-01-02
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditShanxiTaiyuan import CreditShanxiTaiyuan


class Crawler__qyxg_xzcf__credit_shanxitaiyuan(CreditShanxiTaiyuan):
    name = 'Crawler__qyxg_xzcf__credit_shanxitaiyuan'
    start_urls = ['http://www.creditsx.gov.cn/xzcfList.jspx?pageNo=1']

