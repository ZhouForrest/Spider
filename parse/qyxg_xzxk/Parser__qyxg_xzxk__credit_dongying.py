# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    Copyright:        2018, BBD Tech.Co.Ltd

    File Name:        parsers/manual_parser/qyxg_xzxk/Parser__qyxg_xzxk__credit_dongying.py

    Description:      信用中国（东营）-行政许可

    Author:           dengliangwen@bbdservice.com

    Date:             2018-07-31-16:02:39

    Version:          v1.0

    Lastmodified:     2018-07-31 by Jack Deng
-------------------------------------------------
"""

import uuid
import json
import traceback

from datetime import datetime
from hive_framework_milk.commons.utils.tools import gen_rowkey
from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser


class Parser__qyxg_xzxk__credit_dongying(ManualBaseParser):
    """
    class Parser__qyxg_xzxk__credit_dongying for
    信用中国（东营）-行政许可
    """

    name = "Parser__qyxg_xzxk__credit_dongying"
    parser_info = "信用中国（东营）-行政许可"
    base_dict = {
        "version": 1,
    }
    real_url_format = "http://credit.dongying.gov.cn/html/infoPublicity/permitDetails.html?ID={}"

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
            res_list = []
            for data in json_data["results"]:
                determine_date = data.get("DETERMINEDATE", None)
                terminal_date = data.get("TERMINALDATE", None)
                license_start_date = self.date_convert(determine_date)
                license_end_date = self.date_convert(terminal_date)
                res_dict = {
                    "company_name": data.get("LEGALPERSON", "") if data.get("LEGALPERSON", "") else "",
                    "license_org": data.get("ORGNAME", "") if data.get("ORGNAME", "") else "",
                    "license_code": data.get("NO", "") if data.get("NO", "") else "",
                    "case_name": data.get("PROJECTNAME", "") if data.get("PROJECTNAME", "") else "",
                    "approval_category": data.get("AUDITTYPE", "") if data.get("AUDITTYPE", "") else "",
                    "license_content": data.get("NOTE", "") if data.get("NOTE", "") else "",
                    "credit_code": data.get("CREDITCODE", "") if data.get("CREDITCODE", "") else "",
                    "organization_code": data.get("ORGNO", "") if data.get("ORGNO", "") else "",
                    "regno": data.get("ICREGCODE", "") if data.get("ICREGCODE", "") else "",
                    "tax_code": data.get("TAXCODE", "") if data.get("TAXCODE", "") else "",
                    "id_number": data.get("REPRESENTATIVEID", "") if data.get("REPRESENTATIVEID", "") else "",
                    "frname": data.get("REPRESENTATIVE", "") if data.get("REPRESENTATIVE", "") else "",
                    "license_start_date": license_start_date,
                    "license_end_date": license_end_date,
                    "remark": data.get("REMARK", "") if data.get("REMARK", "") else "",
                }
                res_dict.update(source)
                res_dict.update(self.base_dict)
                res_dict["_id"] = "{}".format(uuid.uuid4())
                res_dict["rowkey"] = gen_rowkey(res_dict)
                res_dict["bbd_html"] = ""
                res_dict["bbd_url"] = self.real_url_format.format(data["ID"])
                res_list.append(res_dict)
            return res_list
        except Exception:
            msg = "{} parse error url {}! msg:{}".format(
                self.parser_info, source["bbd_url"], traceback.format_exc())
            self.logger.error(msg)

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
