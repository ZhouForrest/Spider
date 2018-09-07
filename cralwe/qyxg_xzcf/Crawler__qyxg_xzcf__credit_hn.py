# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__credit_hn.py
    Description:    信用湖南 - 行政处罚
    Author:         QL
    Date:           2017-12-26
    version:        v.1.0
-------------------------------------------------
"""

from ..qyxg_xzxk.CreditHuNan import CreditHuNan


class Crawler__qyxg_xzcf__credit_hn(CreditHuNan):
    name = 'Crawler__qyxg_xzcf__credit_hn'
    start_urls = [
        'http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentList.do',  # 信用湖南
        'http://xycs.changsha.gov.cn/sgs/webInfo/punishmentList.do',  # 信用长沙
        'http://credit.zjj.gov.cn/sgs/webInfo/punishmentList.do',  # 信用张家界
        'http://credit.hengyang.gov.cn/sgs/webInfo/punishmentList.do',  # 信用衡阳
        'http://credit.yiyang.gov.cn/sgs/webInfo/punishmentList.do',  # 信用益阳
        'http://credit.shaoyang.gov.cn/sgs/webInfo/punishmentList.do',  # 信用邵阳
        'http://credit.xiangtan.gov.cn/sgs/webInfo/punishmentList.do',  # 信用湘潭
        # 'http://yycredit.yueyang.gov.cn/sgs/webInfo/licenseList.do',  # 信用岳阳：网站打不开，暂不开发
    ]
