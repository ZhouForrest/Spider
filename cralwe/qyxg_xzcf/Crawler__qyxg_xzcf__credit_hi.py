# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_hi.py
    Description:    信用海南-行政处罚
    Author:         Abby
    Date:           2017-12-19
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditHainan import CreditHainan


class Crawler__qyxg_xzcf__credit_hi(CreditHainan):
    name = 'Crawler__qyxg_xzcf__credit_hi'
    start_urls = ['http://xyhn.hainan.gov.cn/JRBWeb/jointCredit/HnZsXzcfxxSjbzMainController.do?reqCode=getXzcfInfo&pageIndex=1&pageSize=10&isIndex=2']
    detail_url = "http://xyhn.hainan.gov.cn/JRBWeb/website/SysXymlResourcesEditController.do?reqCode=showxzxkxx&key='{}'&stype=2"

