# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        parsers/manual_parser/qyxg_xzcf/Parser__qyxg_xzcf__gs_fda.py

    Description:      xzcf-甘肃省食品药品监管局解析

    Author:           dengliangwen@bbdservice.com

    Date:             2018-05-08-10:38:51

    Version:          v1.0

    Lastmodified:     2018-05-08 by Jack Deng

-------------------------------------------------
"""

import re
import uuid
import traceback

from scrapy.selector import Selector

from .field_mapping import map_field
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser
from hive_framework_milk.commons.utils.selector_util import clean_all_space, clean_html


class Parser__qyxg_xzcf__gs_fda(ManualBaseParser):
    """
    class Parser__qyxg_xzcf__gs_fda for 甘肃省食品药品监管局解析
    """

    name = "Parser__qyxg_xzcf__gs_fda"
    parser_info = "xzcf-甘肃省食品药品监管局解析"
    base_dict = {
        'type': "甘肃",
        'version': 1,
    }

    def parse(self, source, *args, **kwargs):
        """
        parse logic
        :Keyword Arguments:
         self     --
         source   --
         *args    --
         **kwargs --
        :return: parsed dict
        """
        try:
            detail_html = clean_html(source.pop('bbd_html', ''))
            detail_url = source.get('bbd_url', '')
            self.logger.info('开始解析:{} {}'.format(self.parser_info, detail_url))
            response = Selector(text=detail_html)
            titles = [
                clean_all_space(re.sub(r':|：', r'', til.strip()))
                for til in response.xpath(
                    '//table//tr[position()>1]//th').xpath('string(.)').extract()
            ]
            values = [
                val.strip() for val in response.xpath(
                    '//table//tr[position()>1]//td').xpath('string(.)').extract()
            ]
            tmp_dict = dict(zip(titles, values))
            res_dict = map_field(tmp_dict)
            res_dict["bbd_seed"] = ""
            res_dict["_id"] = "{}".format(uuid.uuid4())
            res_dict["bbd_html"] = ""
            res_dict.update(source)
            res_dict.update(self.base_dict)
            res_dict["rowkey"] = gen_rowkey(res_dict)
            return res_dict
        except Exception as err:
            msg = '{} parse error! msg:{}'.format(self.parser_info,
                                                  traceback.format_exc())
            self.logger.warning(msg)
