# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__qyxg_xzcf__credit_fengjie.py

    Description:      信用奉节-行政处罚

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-20-09:57:16

    Version:          v1.0

    Lastmodified:     2018-08-20 by Jack Deng

-------------------------------------------------
"""

from .Crawler__credit_fengjie_base import Crawler__credit_fengjie_base as Base


class Crawler__qyxg_xzcf__credit_fengjie(Base):
    """
    class Crawler__qyxg_xzcf__credit_fengjie for
    信用奉节-行政处罚
    """

    name = "Crawler__qyxg_xzcf__credit_fengjie"
    page_url = "http://fengjie.hlxy.com/documents/api/queryCreditPublicity?pageNum={}&typeCode=300003&keyWord="
    detail_url = "http://fengjie.hlxy.com/documents/api/queryDetailByExtraId?id={}"
