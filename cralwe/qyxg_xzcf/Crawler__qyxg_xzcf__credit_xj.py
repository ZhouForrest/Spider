# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_xj.py
    Description:    信用新疆 - 行政处罚
    Author:         QL
    Date:           2017-12-20
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditXinJiang import CreditXinJiang


class Crawler__qyxg_xzcf__credit_xj(CreditXinJiang):
    name = 'Crawler__qyxg_xzcf__credit_xj'
    start_urls = ['http://www.creditxj.gov.cn/doublePublicController/toDoublePublicPage?doubleflag=0']
    detail_url = 'http://www.creditxj.gov.cn/doublePublicController/toadpunishDetail.do?puniId={}'
    post_url = 'http://www.creditxj.gov.cn/doublePublicController/toDoublePublicPage?keyword=&CF_WSH=&CF_XDR='
