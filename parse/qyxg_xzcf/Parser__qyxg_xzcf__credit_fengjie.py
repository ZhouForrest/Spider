# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        hive_worker_hot_coffee/parsers/manual_parser/qyxg_xzcf/Parser__qyxg_xzcf__credit_fengjie.py

    Description:      信用奉节-行政处罚 解析

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-20-10:35:50

    Version:          v1.0

    Lastmodified:     2018-08-20 by Jack Deng

-------------------------------------------------
"""

import uuid
import json
import traceback

from datetime import datetime
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser


class Parser__qyxg_xzcf__credit_fengjie(ManualBaseParser):
    """
    class Parser__qyxg_xzcf__credit_fengjie for
    信用奉节-行政处罚 解析
    """

    name = "Parser__qyxg_xzcf__credit_fengjie"
    parser_info = "信用奉节-行政处罚 解析"
    base_dict = {
        "version": 1,
    }

    def parse(self, source, *args, **kwargs):
        """
        parse logic
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
            data_content = json_data["data"]["dataContentJson"]
            data_func = self.get_value(json_data["data"])
            detail_func = self.get_value(data_content)
            credit_code = detail_func("id_number") if "空" != detail_func(
                "id_number") else data_func("uscCode")
            res_dict = {
                "company_name": detail_func("org_name"),
                "credit_code": credit_code,
                "regno": data_func("regCode"),
                "case_name": detail_func("punish_name"),
                "punish_code": detail_func("decide_docno"),
                "punish_category": detail_func("punish_type1"),
                "punish_type": detail_func("reason"),
                "punish_content": detail_func("punish_ret"),
                "punish_basis": detail_func("gist"),
                "punish_org": detail_func("organization"),
                "punish_date": detail_func("dt_penalty"),
                "punish_status": detail_func("cur_status"),
            }
            res_dict.update(source)
            res_dict.update(self.base_dict)
            res_dict["_id"] = "{}".format(uuid.uuid4())
            res_dict["rowkey"] = gen_rowkey(res_dict)
            res_dict["bbd_html"] = ""
            self.logger.info("save {} to mongo".format(
                res_dict["company_name"]))
            return res_dict
        except Exception as err:
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
             key        --
             inner_dict -- (default json_dict)
            :return: None
            """
            tmp_val = inner_dict.get(key, None)
            if "null" == tmp_val or None == tmp_val:
                return ""
            return tmp_val

        return inner
