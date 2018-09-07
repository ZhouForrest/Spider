# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_sh.py
    Description:    上海诚信网-行政处罚
    Author:         hyy
    Date:           2018-01-09
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditShanghai import CreditShanghai


class Crawler__qyxg_xzcf__credit_sh(CreditShanghai):
    name = 'Crawler__qyxg_xzcf__credit_sh'
    start_urls = ['http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/cflist/cfgrid.action?search=false&rows=200&page=1&sord=asc']
    page_url = 'http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/cflist/cfgrid.action?search=false&rows=200&page={}&sord=asc'
    detail_url = 'http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/sgsinfo/getcfinfo.action?cfid={}'
