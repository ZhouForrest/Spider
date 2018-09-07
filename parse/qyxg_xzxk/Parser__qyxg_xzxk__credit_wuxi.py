# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        parsers/manual_parser/qyxg_xzxk/Parser__qyxg_xzxk__credit_wuxi.py

    Description:      信用巫溪-行政许可 解析

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-21-15:21:08

    Version:          v1.0

    Lastmodified:     2018-08-21 by Jack Deng

-------------------------------------------------
"""

import uuid
import json
import traceback

from datetime import datetime
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser


class Parser__qyxg_xzxk__credit_wuxi(ManualBaseParser):
    """
    class Parser__qyxg_xzxk__credit_wuxi for
    信用巫溪-行政许可 解析
    """

    name = "Parser__qyxg_xzxk__credit_wuxi"
    parser_info = "信用巫溪-行政许可 解析"
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
            credit_code = detail_func("id_number") if "空" != detail_func("id_number") else data_func("uscCode")
            res_dict = {
                "company_name": detail_func("org_name"),
                "credit_code": credit_code,
                "regno": data_func("regCode"),
                "case_name": detail_func("admin_permit_name"),
                "license_code": detail_func("admin_permit_no"),
                "approval_category": detail_func("admin_permit_type"),
                "license_content": detail_func("admin_permit_content"),
                "license_org": detail_func("admin_permit_department"),
                "license_start_date": detail_func("admin_permit_start_time"),
                "license_end_date": detail_func("admin_permit_end_time"),
                "license_status": detail_func("cur_status"),
            }
            res_dict.update(source)
            res_dict.update(self.base_dict)
            res_dict["_id"] = "{}".format(uuid.uuid4())
            res_dict["rowkey"] = gen_rowkey(res_dict)
            res_dict["bbd_html"] = ""
            self.logger.info("save {} to mongo".format(res_dict["company_name"]))
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
