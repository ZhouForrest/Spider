# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        scrapy_spiders/specific_spiders/qyxg_xzcf/Crawler__qyxg_xzxk__credit_jinzhong.py

    Description:      信用晋中-行政许可

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-06-11:17:13

    Version:          v1.0

    Lastmodified:     2018-08-06 by Jack Deng
-------------------------------------------------
"""
from ..qyxg_xzcf.Crawler__credit_jinzhong_base import Crawler__credit_jinzhong_base as Base


class Crawler__qyxg_xzxk__credit_jinzhong(Base):
    """
    class Crawler__qyxg_xzxk__credit_jinzhong for
    信用晋中-行政许可
    """

    name = "Crawler__qyxg_xzxk__credit_jinzhong"
    post_detail_urls = {
        "http://www.creditsxjz.gov.cn/xzxkListNew.jspx":
        "http://www.creditsxjz.gov.cn/xzxkDetialNew-{}.jspx",
        "http://www.creditsxjz.gov.cn/xzxkPListNew.jspx":
        "http://www.creditsxjz.gov.cn/xzxkPDetialNew-{}.jspx",
    }
