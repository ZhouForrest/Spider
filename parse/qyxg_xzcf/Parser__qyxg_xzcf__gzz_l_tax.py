#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__gzz_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__gzz_l_tax(SC_l_tax_base):
    """甘孜州"""
    key_word_map = {
        '行政处罚决定文书号': 'punish_code',
        '行政处罚决定书文号': 'punish_code',
        '政处罚决定文书号': 'punish_code',
        '行政处罚文书号': 'punish_code',
    
        '处罚名称': 'case_name',
        '处罚类别': 'punish_category', '处罚类别1': 'punish_category',
        '罚类别': 'punish_category',
        '处罚事由': 'punish_type',
        '处罚依据': 'punish_basis',
        '行政相对人名称': 'company_name', '行政相对人名': 'company_name',
    
        # '行政相对人代码-1': 'credit_code',
        '（统一社会信用代码）': 'credit_code',
        '行政相对人代码-1（统一社会信用代码）': 'credit_code',
        '行政相对人代码/1（统一社会信用代码）': 'credit_code', '行统一社会信用代码': 'credit_code',
        '统一社会信用代码': 'credit_code',
        '统一社会代码': 'credit_code',
        '行政相对人代码-1（社会统一信用代码）': 'credit_code',
        '行政相对人代码（统一社会信用代码）': 'credit_code', '统一社会信用代': 'credit_code', '行政相对人代码1（统一社会信用代码）': 'credit_code',
    
        '行政相对人统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信用代码）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信息代码）': 'credit_code',  # 需要特殊处理，乐山
    
    
        '行政相对人代码-2（组织机构代码）': 'organization_code',
        '行政相对人代码/2（组织机构代码）': 'organization_code',
        # '行政相对人代码-2': 'organization_code',
    
        '（纳税人识别号）': 'tax_code',
        '行政相对人代码-3': 'tax_code',
        '行政相对人代码-3（纳税人识别号）': 'tax_code',
        '行政相对人代码/3（纳税人识别号）': 'tax_code',
        '统一社会信用代码（纳税人识别码）': 'tax_code',
        '纳税人识别号': 'tax_code',
        '行政相对人代码（纳税人识别号）': 'tax_code',
    
        '行政相对人代码-4（居民身份证号）': 'id_number',
        '行政相对人代码/4（居民身份证号）': 'id_number',
        '（居民身份证）': 'id_number',
        '行政相对人代码-4 ': 'id_number',
        '行政相对人代码-4': 'id_number',
    
        '法定代表人姓名': 'frname',
        '法定代表人': 'frname',
        '处罚结果': 'punish_content',
        '兴处罚决定日期': 'punish_date',
        '处罚决定日期': 'punish_date', '处罚日期': 'punish_date',
        '处罚机关': 'punish_org',
        '当前状态': 'punish_status',
        '地方编码': 'administrative_code',
        '数据更新时间': 'update',
        '数据更新时间戳': 'update',
        '公示期限': 'public_period',
        '备注': 'remark',
    
    }
