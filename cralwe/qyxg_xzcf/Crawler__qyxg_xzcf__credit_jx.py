# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_jx.py
    Description:    信用江西-行政处罚
    Author:         Abby
    Date:           2017-01-03
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditJiangxi import CreditJiangxi


class Crawler__qyxg_xzcf__credit_jx(CreditJiangxi):
    name = 'Crawler__qyxg_xzcf__credit_jx'
    start_url = 'http://www.creditjx.gov.cn/datareporting/doublePublicity/queryDoublePublicityList.json'
    detail_url = "http://www.creditjx.gov.cn/datareporting/doublePublicity/punishDetail/{}"
    form_data = {
        "tableType": "1",
        "inpParam": "",
        "orgIdOrRegionId": "",
        "page": "1",
        "pageSize": "15"
    }
