# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_sh.py
    Description:    上海诚信网-行政许可
    Author:         hyy
    Date:           2018-01-09
    version:        v.1.0
-------------------------------------------------
"""
from .CreditShanghai import CreditShanghai


class Crawler__qyxg_xzxk__credit_sh(CreditShanghai):
    name = 'Crawler__qyxg_xzxk__credit_sh'
    start_urls = ['http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/xklist/xkgrid.action?search=false&rows=200&page=1&sord=asc']
    page_url = 'http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/xklist/xkgrid.action?search=false&rows=200&page={}&sord=asc'
    detail_url = 'http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/sgsinfo/getxkinfo.action?xkid={}'
