# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzxk__credit_gd.py
    Description:    信用广东--行政许可
    Author:         Jack Deng
    Date:           2017-12-19
    Version:        v.1.0
    Lastmodified:   2017-12-20 by Jack Deng
-------------------------------------------------
"""

from .CreditGuangdong import CreditGuangdong

class Crawler__qyxg_xzxk__credit_gd(CreditGuangdong):
    """
    信用广东--行政许可
    """

    name = "Crawler__qyxg_xzxk__credit_gd"
    start_urls = ["http://www.gdcredit.gov.cn/infoTypeAction!xzTwoPublicList.do?type=3"]