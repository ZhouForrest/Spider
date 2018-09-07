# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzxk/Crawler__qyxg_xzxk__credit_fengjie.py

    Description:      信用奉节-行政许可

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-20-10:18:33

    Version:          v1.0

    Lastmodified:     2018-08-20 by Jack Deng

-------------------------------------------------
"""

from ..qyxg_xzcf.Crawler__credit_fengjie_base import Crawler__credit_fengjie_base as Base

class Crawler__qyxg_xzxk__credit_fengjie(Base):
    """
    class Crawler__qyxg_xzxk__credit_fengjie for
    信用奉节-行政许可
    """

    name = "Crawler__qyxg_xzxk__credit_fengjie"
    page_url = "http://fengjie.hlxy.com/documents/api/queryCreditPublicity?pageNum={}&typeCode=300008&keyWord="
    detail_url = "http://fengjie.hlxy.com/documents/api/queryDetailByExtraId?id={}"
