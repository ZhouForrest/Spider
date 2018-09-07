# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__qyxg_xzcf__credit_wuxi.py

    Description:      信用巫溪-行政处罚

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-21-15:00:25

    Version:          v1.0

    Lastmodified:     2018-08-21 by Jack Deng

-------------------------------------------------
"""

from .Crawler__credit_wuxi_base import Crawler__credit_wuxi_base as Base


class Crawler__qyxg_xzcf__credit_wuxi(Base):
    """
    class Crawler__qyxg_xzcf__credit_wuxi for
    信用巫溪-行政处罚
    """

    name = "Crawler__qyxg_xzcf__credit_wuxi"
    page_url = "http://wuxi.hlxy.com/documents/api/queryCreditPublicity?pageNum={}&typeCode=300003&keyWord="
    detail_url = "http://wuxi.hlxy.com/documents/api/queryDetailByExtraId?id={}"
