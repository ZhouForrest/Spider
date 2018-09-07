# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_gz.py
    Description:    信用贵州-行政处罚
    Author:         Abby
    Date:           2017-12-19
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditGuizhou import CreditGuizhou


class Crawler__qyxg_xzcf__credit_gz(CreditGuizhou):
    name = 'Crawler__qyxg_xzcf__credit_gz'
    start_urls = ['http://58.42.237.143:8080/gs/gdsgs/xzcfxx/list?ip_name=http://www.gzcx.gov.cn&area_code=']
    post_url = "http://58.42.237.143:8080/gs/gdsgs/xzcfxx/list"
    form_data = {
        "pageNo": "2",
        "pageSize": "10",
        "area_code": "",
        "sjfw": "",
        "beginDate": "",
        "endDate": "",
        "depname": "",
        "cfWsh": ""
    }
