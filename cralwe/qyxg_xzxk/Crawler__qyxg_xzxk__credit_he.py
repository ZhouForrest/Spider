# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_he.py
    Description:    双公示-信用河北-行政许可
    Author:         Jack Deng
    Date:           2018-01-02
    version:        v.1.0

    lastmodified:       2018-01-02  by  Jack Deng
-------------------------------------------------
"""

from .CreditHebei import CreditHebei

class Crawler__qyxg_xzxk__credit_he(CreditHebei):
    """
    双公示-信用河北-行政许可
    """

    name = "Crawler__qyxg_xzxk__credit_he"

    def custom_init(self, *args, **kwargs):
        self.seed_key = "qyxg_xzxk__credit_he"
        self.search_url = "http://123.182.226.146:8082/was5/web/search?perpage=6&channelid=284126&orderby=RELEVANCE&searchword={}"
        super(Crawler__qyxg_xzxk__credit_he, self).custom_init(*args, **kwargs)