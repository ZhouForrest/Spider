# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      CreditZhejiang.py
    Description:    信用浙江
    Author:         crazy_jacky
    Date:           2018-01-09
    version:        v.1.0
-------------------------------------------------
"""
import re
import traceback

from scrapy import FormRequest
from scrapy.http.request import Request

from hive_framework_milk.commons.utils.tools import calc_str_md5
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from .field_mapping import map_field


class CreditZhejiang(SpiderAll):
    """
    Credit zhe jiang info base class.
    """
    name = 'CreditZhejiang'
    specific_settings = {
        'COOKIES_ENABLED': True,
    }

    def parse(self, response):
        try:
            key_cont = ''.join(response.xpath('.//script[@language="javascript"]//text()').extract())
            total_record = ''.join(re.compile('totalRecord:\d+').findall(key_cont)).split(":")[-1]
            proxy_url = ''.join(re.compile("proxyUrl:.*?,").findall(key_cont)).split("'")[-2]
            id2 = ''.join(re.compile("id2:'\w+").findall(key_cont)).split("'")[-1]
            url = response.urljoin(proxy_url)
            per_page = 20
            form_data = {'startrecord': '',
                         'endrecord': '',
                         'perpage': str(per_page),
                         'totalRecord': total_record,
                         'id2': id2}

            pages, more = divmod(int(total_record), per_page)
            if more:
                pages += 1
            for page in range(1, pages + 1):
                startrecord = (page - 1) * per_page + 1
                endrecord = page * per_page
                form_data.update({'startrecord': str(startrecord), 'endrecord': str(endrecord)})
                self.logger1.info('begin to request page num:{}'.format(page))
                yield FormRequest(url, callback=self.parse_lst, formdata=form_data, errback=self.error_parse,
                                  dont_filter=True)
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on get the page counts[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_lst(self, response):
        """
        parse detail page link
        :param response:
        :return:
        """
        try:
            self.logger1.info("Start to parse the lst link of {}".format(response.url))
            link_list = re.compile('/.*?=\w+').findall(response.text)
            for link in link_list:
                detail_url = response.urljoin(link.strip())
                yield Request(detail_url, callback=self.parse_detail, errback=self.error_parse,
                              priority=6, meta={'count': 0})
        except:
            err_msg = traceback.format_exc()
            self.logger1.warning("Exception occurred on parse the link page[{url}], error:{err_msg}".format(
                url=response.url, err_msg=err_msg))

    def parse_detail(self, response):
        """
        parse detail page
        :param response:
        :return:
        """
        try:
            self.logger1.info('start to parse detail content {}'.format(response.url))
            cmp_name = ''.join(response.xpath('.//td[@class="listf2"]//text()').extract()).strip()
            punish_rst = ''.join(response.xpath('//td[@class="xzcf_jds"]//text()').extract())
            cont_type = ''.join(response.xpath('//td[@width="270"]//text()').extract())
            tr_list = response.xpath('//table[@class="xzcf_bg"]//tr')
            special = tr_list.pop(1)
            key_lst = [''.join(item.xpath('string(.)').extract()).strip(u'：') for item in tr_list.xpath('.//td[2]')]
            val_lst = [''.join(item.xpath('string(.)').extract()).strip() for item in tr_list.xpath('.//td[3]')]
            special_dic = self.deal_special(special)
            detail_dic = dict(zip(key_lst, val_lst))
            detail_dic.update(special_dic)
            if u'行政处罚' in cont_type:
                key = 'punish_content'
            else:
                key = 'license_content'
            detail_dic.update({'case_name': cmp_name, key: punish_rst})
            result = map_field(detail_dic)
            item = self.result_item_assembler(response)
            item['_id'] = calc_str_md5(response.url)
            item['bbd_html'] = ''
            item['_parsed_data'] = result
            yield item
            self.logger1.info('{} save successfully'.format(response.url))
        except Exception as e:
            self.logger1.warning("Exception on save detail page {} {} {}".format(
                response.url, traceback.format_exc(), e))

    def deal_special(self, special):
        """
        deal abnormal tr content
        :param special:
        :return:
        """
        special_dic = {}
        try:
            self.logger1.info('begin to parse special tr')
            cont_lst = list(filter(None, ''.join(special.xpath('string(.)').extract()).strip().split(u'\xa0')))
            for cont in cont_lst:
                item = cont.split(u'：')
                if len(item) > 1:
                    special_dic[item[0].strip()] = item[1].strip()
                else:
                    special_dic[item[0].strip()] = ''
            return special_dic
        except:
            self.logger1.info('parse special tr failed')
            return special_dic

    def error_parse(self, response):
        self.logger1.warning('request {} failed'.format(response.request.url))
