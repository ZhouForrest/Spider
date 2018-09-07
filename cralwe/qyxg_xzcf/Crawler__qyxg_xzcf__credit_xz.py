# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_xz.py
    Description:    信用西藏-行政处罚
    Author:         Abby
    Date:           2017-12-20
    version:        v.1.0
-------------------------------------------------
"""
from ..qyxg_xzxk.CreditXizang import CreditXizang


class Crawler__qyxg_xzcf__credit_xz(CreditXizang):
    name = 'Crawler__qyxg_xzcf__credit_xz'
    specific_settings = {'COOKIES_ENABLED': True}
    start_urls = ['http://www.creditxizang.gov.cn/doublePublicController/toDoublePublicPage?doubleflag=0']
    post_url = "http://www.creditxizang.gov.cn/doublePublicController/toDoublePublicPage?keyword="
    form_data = {
        "pageNum": "2",
        "numPerPage": "10",
        "orderField": "",
        "orderDirection": "",
        "prePage": "1",
        "nextPage": "2",
        "ttPage": "6"
    }
    # header = {
    #     "Host": "www.creditxizang.gov.cn",
    #     "Connection": "keep-alive",
    #     "Upgrade-Insecure-Requests": "1",
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.9"
    # }
