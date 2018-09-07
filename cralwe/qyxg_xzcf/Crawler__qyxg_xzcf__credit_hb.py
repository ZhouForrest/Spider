# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_hb.py
    Description:    信用湖北-行政处罚
    Author:         Abby
    Date:           2017-01-02
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditHubei import CreditHubei


class Crawler__qyxg_xzcf__credit_hb(CreditHubei):
    name = 'Crawler__qyxg_xzcf__credit_hb'
    start_urls = ['http://www.hbcredit.gov.cn/credithb/gkgs/list.html?type=PublicityPunishment']
    form_data = {
        "bt": "",
        "bmmc": "",
        "sxmc": "",
        "type": "PublicityPunishment",
        "pageIndex": "1"
    }
