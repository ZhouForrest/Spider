# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_gs.py
    Description:    信用甘肃 - 行政许可
    Author:         QL
    Date:           2018-01-08
    version:        v.1.0
-------------------------------------------------
"""

from .CreditGanSu import CreditGanSu


class Crawler__qyxg_xzxk__credit_gs(CreditGanSu):
    name = 'Crawler__qyxg_xzxk__credit_gs'
    start_urls = [
        'http://www.gscredit.gov.cn/sgs/xzxk/list.jspx?type=legal',
        'http://www.gscredit.gov.cn/sgs/xzxk/list.jspx?type=person'
    ]
