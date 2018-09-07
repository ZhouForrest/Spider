# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_jx.py
    Description:    信用江西-行政许可
    Author:         Abby
    Date:           2017-01-03
    version:        v.1.0
-------------------------------------------------
"""
from .CreditJiangxi import CreditJiangxi


class Crawler__qyxg_xzxk__credit_jx(CreditJiangxi):
    name = 'Crawler__qyxg_xzxk__credit_jx'
    start_url = 'http://www.creditjx.gov.cn/datareporting/doublePublicity/queryDoublePublicityList.json'
    detail_url = "http://www.creditjx.gov.cn/datareporting/doublePublicity/permissionDetail/{}"
    form_data = {
        "tableType": "2",
        "inpParam": "",
        "orgIdOrRegionId": "",
        "page": "1",
        "pageSize": "15"
    }
