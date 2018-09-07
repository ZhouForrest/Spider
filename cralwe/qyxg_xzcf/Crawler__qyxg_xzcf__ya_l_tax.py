#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Crawler__qyxg_xzcf__dz_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-04 9:57
:Version: v.1.0
:Description: 
"""
import re
import hashlib
from hive_framework_milk.commons.state import STATE
from hive_framework_milk.scrapy_spiders.item import ImageSeedItem
from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzcf.Crawler__qyxg_xzcf__dz_l_tax import Crawler__qyxg_xzcf__dz_l_tax


class Crawler__qyxg_xzcf__ya_l_tax(Crawler__qyxg_xzcf__dz_l_tax):
    """四川省地方税务局-税务行政处罚公告数据 - 雅安"""
    name = 'Crawler__qyxg_xzcf__ya_l_tax'
    
    start_urls = ['http://ya.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index.html']
    
    next_page_tpl = 'http://ya.sc-l-tax.gov.cn/cdssxc/xzgs/xzcfgs/index_{}.html'
  
    def parse_attach_page(self, response, source_dict):
        script_str = re.sub('\s+', '', ''.join(response.xpath('string(//div[@class="content"]//script)').extract()))
        attach_url_re = re.match('.*href="(\./\w+\..*)"target.*', script_str)
        if attach_url_re:
            attach_url = response.urljoin(attach_url_re.groups()[0])
            attach_title = re.match('.*>(.*\..*)</a.*', script_str).groups()[0]
            md = hashlib.md5()
            md.update(attach_title.encode() + attach_url.encode())
            attach_data = {
                'attachment_title': attach_title,
                "attachment_url": attach_url,
                "attachment_id": md.hexdigest(),
                "upload_status": STATE.INITIAL,
                "download_status": STATE.INITIAL,
            }
            source_dict['attachment_list'] = [attach_data]
            source_dict['bbd_html'] = ''
            item = ImageSeedItem()
            item['seed_data'] = {
                'bbd_table': 'attach',
                'bbd_type': 'seed',
                'bbd_url': response.request.url,
                'seed_data': source_dict
            }
            return item
        else:
            self.logger1.log_more('Attach url parse failed, url:{}'.format(response.request.url), level='warn')
            # source_dict['main'] = response.xpath('string(//div[@class="content"]//p)').extract_first().strip()
            
        