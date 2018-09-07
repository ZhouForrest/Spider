# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_xz.py
    Description:    信用西藏-行政许可
    Author:         Abby
    Date:           2017-12-20
    version:        v.1.0
-------------------------------------------------
"""
from .CreditXizang import CreditXizang


class Crawler__qyxg_xzxk__credit_xz(CreditXizang):
    name = 'Crawler__qyxg_xzxk__credit_xz'
    specific_settings = {'COOKIES_ENABLED': True}
    start_urls = ['http://www.creditxizang.gov.cn/doublePublicController/toDoublePublicPage2?doubleflag=1']
    post_url = "http://www.creditxizang.gov.cn/doublePublicController/toDoublePublicPage2?&keyword="
    form_data = {
        "pageNum": "2",
        "numPerPage": "10",
        "orderField": "",
        "orderDirection": "",
        "prePage": "1",
        "nextPage": "2",
        "ttPage": "24544"
    }
