# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_hb_search.py
    Description:    信用湖北-行政许可
    Author:         Abby
    Date:           2017-01-09
    version:        v.1.0
-------------------------------------------------
"""
from .CreditHubeiSearch import CreditHubeiSearch


class Crawler__qyxg_xzxk__credit_hb_search(CreditHubeiSearch):
    name = 'Crawler__qyxg_xzxk__credit_hb_search'
    form_data = {
        "bt": "",
        "bmmc": "",
        "sxmc": "",
        "type": "PublicityLicense",
        "pageIndex": "1"
    }

    def custom_init(self, *args, **kwargs):
        self.seed_key = "xzxk_hubei"
        self.search_url = "http://www.hbcredit.gov.cn/credithb/gkgs/list.html"
        super(Crawler__qyxg_xzxk__credit_hb_search, self).custom_init(*args, **kwargs)
