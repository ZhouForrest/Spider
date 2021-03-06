#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__zy_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-26 9:39
:Version: v.1.0
:Description: 
"""

from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzcf.sc_l_base_crawl import SCLocalBaseCrawl


class Crawler__qyxg_xzcf__sn_l_tax(SCLocalBaseCrawl):
    """四川省地方税务局-税务行政处罚公告数据 - 遂宁"""
    name = 'Crawler__qyxg_xzcf__sn_l_tax'
    
    start_urls = ['http://sn.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcf/index.html']
    
    next_page_tpl = 'http://sn.sc-l-tax.gov.cn/cdssxc/cdrdzt/xzgs/xzcf/index_{}.html'

    

    
