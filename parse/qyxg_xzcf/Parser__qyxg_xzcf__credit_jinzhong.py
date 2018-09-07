# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        parsers/manual_parser/qyxg_xzcf/Parser__qyxg_xzcf__credit_jinzhong.py

    Description:      信用晋中-行政处罚 解析

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-06-15:44:08

    Version:          v1.0

    Lastmodified:     2018-08-06 by Jack Deng
-------------------------------------------------
"""

import uuid
import json
import traceback

from datetime import datetime
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser


class Parser__qyxg_xzcf__credit_jinzhong(ManualBaseParser):
    """
    class Parser__qyxg_xzcf__credit_jinzhong for
    信用晋中-行政处罚
    """

    name = "Parser__qyxg_xzcf__credit_jinzhong"
    parser_info = "信用晋中-行政处罚 解析"
    base_dict = {
        "version": 1,
    }

    def parse(self, source, *args, **kwargs):
        """

        :Keyword Arguments:
         self     --
         source   --
         *args    --
         **kwargs --
        :return: None
        """
        try:
            detail_html = source.pop('bbd_html', '')
            detail_url = source.get('bbd_url', '')
            self.logger.info('开始解析:{} {}'.format(self.parser_info, detail_url))
            json_data = json.loads(detail_html)
            get_func = self.get_value(json_data)
            res_dict = {
                "punish_code": get_func("cfWsh"),
                "case_name": get_func("cfAjmc"),
                "punish_category_one": get_func("cfCflb"),
                "punish_type": get_func("cfSy"),
                "punish_basis": get_func("cfYj"),
                "company_name": get_func("cfXdrMc"),
                "credit_code": get_func("cfXdrShxym"),
                "punish_content": get_func("cfJg"),
                "punish_date": get_func("cfSxq"),
                "punish_org": get_func("cfXzjg"),
                "punish_status": get_func("cfZt"),
                "administrative_code": get_func("dfbm"),
                "data_source": get_func("depName"),
                "pubdate": get_func("publishDate"),
            }
            res_dict.update(source)
            res_dict.update(self.base_dict)
            res_dict["_id"] = "{}".format(uuid.uuid4())
            res_dict["rowkey"] = gen_rowkey(res_dict)
            res_dict["bbd_html"] = ""
            self.logger.info("save {} to mongo".format(res_dict["company_name"]))
            return res_dict
        except Exception:
            msg = "{} parse error url {}! msg:{}".format(
                self.parser_info, source["bbd_url"], traceback.format_exc())
            self.logger.error(msg)

    def get_value(self, json_dict):
        """

        :Keyword Arguments:
         self      --
         json_dict --
        :return: None
        """
        def inner(key, inner_dict=json_dict):
            """

            :Keyword Arguments:
             json_dict --
             key       --
            :return: None
            """
            tmp_val = inner_dict.get(key, None)
            if "null" == tmp_val or None == tmp_val:
                return ""
            return tmp_val
        return inner
