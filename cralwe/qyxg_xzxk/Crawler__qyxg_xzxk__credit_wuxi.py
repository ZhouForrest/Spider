# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzxk/Crawler__qyxg_xzxk__credit_wuxi.py

    Description:      信用巫溪-行政许可

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-21-15:05:55

    Version:          v1.0

    Lastmodified:     2018-08-21 by Jack Deng

-------------------------------------------------
"""

from ..qyxg_xzcf.Crawler__credit_wuxi_base import Crawler__credit_wuxi_base as Base


class Crawler__qyxg_xzxk__credit_wuxi(Base):
    """
    class Crawler__qyxg_xzxk__credit_wuxi for
    信用巫溪-行政许可
    """

    name = "Crawler__qyxg_xzxk__credit_wuxi"
    page_url = "http://wuxi.hlxy.com/documents/api/queryCreditPublicity?pageNum={}&typeCode=300008&keyWord="
    detail_url = "http://wuxi.hlxy.com/documents/api/queryDetailByExtraId?id={}"
