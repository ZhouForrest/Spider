# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__qyxg_xzcf__credit_jinzhong.py

    Description:      信用晋中-行政处罚

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-06-15:02:19

    Version:          v1.0

    Lastmodified:     2018-08-06 by Jack Deng
-------------------------------------------------
"""

from .Crawler__credit_jinzhong_base import Crawler__credit_jinzhong_base as Base


class Crawler__qyxg_xzcf__credit_jinzhong(Base):
    """
    class Crawler__qyxg_xzcf__credit_jinzhong for
    信用晋中-行政处罚
    """

    name = "Crawler__qyxg_xzcf__credit_jinzhong"
    post_detail_urls = {
        "http://www.creditsxjz.gov.cn/xzcfListNew.jspx":
        "http://www.creditsxjz.gov.cn/xzcfDetialNew-{}.jspx",
    }
