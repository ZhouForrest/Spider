# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_jx_search.py
    Description:    信用江西-行政处罚
    Author:         Abby
    Date:           2017-01-09
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditJiangxiSearch import CreditJiangxiSearch


class Crawler__qyxg_xzcf__credit_jx_search(CreditJiangxiSearch):
    name = 'Crawler__qyxg_xzcf__credit_jx_search'

    detail_url = "http://www.creditjx.gov.cn/datareporting/doublePublicity/punishDetail/{}"
    form_data = {
        "tableType": "1",
        "inpParam": "",
        "orgIdOrRegionId": "",
        "page": "1",
        "pageSize": "15"
    }

    def custom_init(self, *args, **kwargs):
        self.seed_key = "xzcf_jiangxi"
        self.search_url = "http://www.creditjx.gov.cn/datareporting/doublePublicity/queryDoublePublicityList.json"
        super(Crawler__qyxg_xzcf__credit_jx_search, self).custom_init(*args, **kwargs)
