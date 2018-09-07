# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        parsers/manual_parser/qyxg_xzcf/Parser__qyxg_xzcf__credit_dongying.py

    Description:      行政处罚-信用中国（东营）解析

    Author:           dengliangwen@bbdservice.com

    Date:             2018-08-03-13:33:56

    Version:          v1.0

    Lastmodified:     2018-08-03 by Jack Deng
-------------------------------------------------
"""

import uuid
import json
import traceback

from datetime import datetime
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser


class Parser__qyxg_xzcf__credit_dongying(ManualBaseParser):
    """
    class Parser__qyxg_xzcf__credit_dongying for
    行政处罚-信用中国（东营）解析
    """

    name = "Parser__qyxg_xzcf__credit_dongying"
    parser_info = "行政处罚-信用中国（东营）解析"
    base_dict = {
        "version": 1,
    }
    real_url_format = "http://credit.dongying.gov.cn/html/infoPublicity/punishDetails.html?ID={}"

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
            json_data = json.loads(detail_html)["results"]
            res_dict = {
                "company_name": self.get_value(json_data, "LEGALPERSON"),
                "punish_org": self.get_value(json_data, "ORGNAME"),
                "case_name": self.get_value(json_data, "PUNISHNAME"),
                "punish_code": self.get_value(json_data, "NO"),
                "punish_category_one": self.get_value(json_data, "AUDITTYPE"),
                "punish_type": self.get_value(json_data, "REASON"),
                "punish_basis": self.get_value(json_data, "ACCORDING"),
                "credit_code": self.get_value(json_data, "CREDITCODE"),
                "organization_code": self.get_value(json_data, "ORGNO"),
                "regno": self.get_value(json_data, "ICREGCODE"),
                "tax_code": self.get_value(json_data, "TAXCODE"),
                "id_number": self.get_value(json_data, "REPRESENTATIVEID"),
                "frname": self.get_value(json_data, "REPRESENTATIVE"),
                "punish_content": self.get_value(json_data, "NOTE"),
                "punish_date": self.date_convert(self.get_value(json_data, "PUNISHDATE")),
                "remark": self.get_value(json_data, "REMARK"),
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

    def get_value(self, data_dic, key):
        """

        :Keyword Arguments:
         self     --
         data_dic --
        :return: None
        """
        tmp_val = data_dic.get(key, None)
        if "null" == tmp_val or None == tmp_val:
            return ""
        return tmp_val

    def date_convert(self, timestamp):
        """

        :Keyword Arguments:
         self      --
         timestamp --
        :return: None
        """
        if not timestamp:
            return ""
        if isinstance(timestamp, str):
            return timestamp
        timestamp = timestamp / 1000
        dt = datetime.fromtimestamp(float(timestamp))
        return dt.strftime("%Y-%m-%d")
