# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_hb.py
    Description:    信用湖北-行政许可
    Author:         Abby
    Date:           2017-01-02
    version:        v.1.0
-------------------------------------------------
"""
from .CreditHubei import CreditHubei


class Crawler__qyxg_xzxk__credit_hb(CreditHubei):
    name = 'Crawler__qyxg_xzxk__credit_hb'
    # start_urls = ['http://www.hbcredit.gov.cn/credithb/gkgs/list.html']
    start_urls = ['http://www.hbcredit.gov.cn/credithb/gkgs/list.html?type=PublicityLicense']
    form_data = {
        "bt": "",
        "bmmc": "",
        "sxmc": "",
        "type": "PublicityLicense",
        "pageIndex": "1"
    }
