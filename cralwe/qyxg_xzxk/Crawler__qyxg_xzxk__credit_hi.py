# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_hi.py
    Description:    信用海南-行政许可
    Author:         Abby
    Date:           2017-12-19
    version:        v.1.0
-------------------------------------------------
"""
from .CreditHainan import CreditHainan


class Crawler__qyxg_xzxk__credit_hi(CreditHainan):
    name = 'Crawler__qyxg_xzxk__credit_hi'
    start_urls = ['http://xyhn.hainan.gov.cn/JRBWeb/JointPunishment/HnZsXzxkxxSjbzMainController.do?reqCode=getXzxkInfo&main_code=&pageIndex=1&pageSize=10']
    detail_url = "http://xyhn.hainan.gov.cn/JRBWeb/website/SysXymlResourcesEditController.do?reqCode=showxzxkxx&key='{}'&stype=1"

