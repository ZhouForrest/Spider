# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_gs.py
    Description:    信用甘肃 - 行政处罚
    Author:         QL
    Date:           2018-01-08
    version:        v.1.0
-------------------------------------------------
"""

from ..qyxg_xzxk.CreditGanSu import CreditGanSu


class Crawler__qyxg_xzcf__credit_gs(CreditGanSu):
    name = 'Crawler__qyxg_xzcf__credit_gs'
    start_urls = [
        'http://www.gscredit.gov.cn/sgs/xzcf/list.jspx?type=legal',
        'http://www.gscredit.gov.cn/sgs/xzcf/list.jspx?type=person'
    ]
