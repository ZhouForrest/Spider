# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_bj_search.py
    Description:    信用北京-行政许可
    Author:         Jack Deng
    Date:           2017-02-08
    version:        v.1.0
-------------------------------------------------
"""
from .CreditBeijingSearch import CreditBeijingSearch


class Crawler__qyxg_xzxk__credit_bj_search(CreditBeijingSearch):
    name = 'Crawler__qyxg_xzxk__credit_bj_search'
    form_data = {
        "typeId":       "19",
        "regionId":     "1",
        "objId":        "1",
        "pageNo":       "1",
        "qname":        "",
        "twoTypeId3":   "733",
        "twoTypeId4":   "741",
        "twoTypeId5":   "19",
        "twoTypeId761": "767",
        "twoTypeId69":  "71",
        "regionType":   "true",
        "objType":      "true",
    }

    def custom_init(self, *args, **kwargs):
        self.seed_key = "xzxk_Beijing"
        self.search_url = "http://cxcj.creditbj.gov.cn/xyData/front/search/list.shtml"
        super(Crawler__qyxg_xzxk__credit_bj_search, self).custom_init(*args, **kwargs)
