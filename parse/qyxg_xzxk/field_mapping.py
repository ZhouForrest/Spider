#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: field_mapping.py.py
:Description: 
:Author: liqingqing@bbdservice.com
:Date: 2018-05-24 上午11:03
:Version: v.1.0
"""

field_mapping = {
    "行政许可决定书文号：": "license_code",
    "项目名称：": "case_name",
    "审批类别：": "approval_category",
    "许可内容：": 'license_content',
    "行政相对人名称：": 'company_name',
    "行政相对人代码_1(统一社会信用代码)：":'credit_code',
    "行政相对人代码_2(组织机构代码)：": 'organization_code',
    "行政相对人代码_3(工商登记码)：":  'regno',
    "行政相对人代码_4(税务登记号)：":'tax_code',
    "行政相对人代码_5 (居民身份证号)：": 'id_number',
    "法定代表人姓名：": 'frname',
    "许可决定日期：": 'license_start_date',
    "许可截止期：": 'license_end_date',
    "许可机关：": 'license_org',
    "当前状态：": 'license_status',
    "地方编码：": 'administrative_code',
    "数据更新时间戳：": 'update',
    "备注：": 'remark'
}


def map_field(result_dict):
    if not isinstance(result_dict, dict):
        raise TypeError('except a dict to map the field')
    temp_result_dict = {}
    for key, value in result_dict.items():
        if field_mapping.get(key, ""):
            temp_result_dict[field_mapping.get(key)] = value
    return temp_result_dict


def replace_space(old_str):
    del_rn = old_str.replace('\r\n', '')
    new_str = del_rn.replace('\t', '')
    return new_str
