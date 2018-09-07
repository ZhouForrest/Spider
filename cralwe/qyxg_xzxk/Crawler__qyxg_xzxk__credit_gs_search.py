# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_gs_search.py
    Description:    信用甘肃 - 行政许可 搜索版
    Author:         QL
    Date:           2018-01-10
    version:        v.1.0
-------------------------------------------------
"""

from .CreditGanSuSearch import CreditGanSuSearch


class Crawler__qyxg_xzxk__credit_gs_search(CreditGanSuSearch):
    name = 'Crawler__qyxg_xzxk__credit_gs_search'

    def custom_init(self, *args, **kwargs):
        self.seed_key = 'qyxg_xzxk__credit_gs'

        # 搜索url分为 法人 和 自然人 两类
        self.search_url_4_legal = 'http://www.gscredit.gov.cn/sgs/xzxk/list.jspx?type=legal'
        self.search_url_4_person = 'http://www.gscredit.gov.cn/sgs/xzxk/list.jspx?type=person'
        super().custom_init(*args, **kwargs)
