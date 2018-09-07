# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_xj.py
    Description:    信用新疆 - 行政许可
    Author:         QL
    Date:           2017-12-20
    version:        v.1.0
-------------------------------------------------
"""
from .CreditXinJiang import CreditXinJiang


class Crawler__qyxg_xzxk__credit_xj(CreditXinJiang):
    name = 'Crawler__qyxg_xzxk__credit_xj'
    start_urls = ['http://www.creditxj.gov.cn/doublePublicController/toDoublePublicPage2?doubleflag=1']
    detail_url = 'http://www.creditxj.gov.cn/doublePublicController/toADlicensingDetail.do?liceId={}'
    post_url = 'http://www.creditxj.gov.cn/doublePublicController/toDoublePublicPage2?&keyword=&CF_WSH=&CF_XDR='
