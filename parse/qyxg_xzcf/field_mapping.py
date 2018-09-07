"""
-------------------------------------------------
    File Name:      field_mapping.py
    Description:    银监会-行政处罚,字段映射
                    如果需要增加字段映射，请修改 field_mapping 字典
    Author:         Jack Deng
    Date:           2017-09-18
-------------------------------------------------
"""

field_mapping = {
    "案件名称": "case_name",
    "行政处罚决定书文号": "punish_code",
    "企业名称或自然人姓名": "name",
    "统一社会信用代码": "credit_code",
    "法定代表人": "frname",
    "行政处罚的种类和依据": "punish_basis",
    "作出处罚决定的部门": "punish_org",
    "做出处罚的日期": "punish_date",
    "主要违法事实": "punish_type",
    "行政处罚的履行方式": "perform_way",
    "行政处罚的履行期限": "perform_deadline",
    "行政执法机关名称": "public_org",
    "备注": "remark",
    "行政处罚决定书文号：": "punish_code",
    "处罚名称：": "case_name",
    "处罚类别1：": "punish_category_one",
    "处罚类别2：": 'punish_category_two',
    "处罚事由：": 'punish_type',
    "处罚依据：": 'punish_basis',
    "行政相对人代码_1(统一社会信用代码)：": 'credit_code',
    "行政相对人代码_2(组织机构代码)：":  'organization_code',
    "行政相对人代码_3(工商登记码)：":'regno',
    "行政相对人代码_4(税务登记号)：": 'tax_code',
    "行政相对人代码_5 (居民身份证号)：": 'id_number',
    "法定代表人姓名：": 'frname',
    "处罚结果：": 'punish_content',
    "处罚机关：": 'punish_org',
    "当前状态：": 'punish_status',
    "地方编码：": 'administrative_code',
    "数据更新时间戳：": 'update',
}


def map_field(result_dict):
    if not isinstance(result_dict, dict):
        raise TypeError('except a dict to map the field')
    temp_result_dict = {}
    for key, value in result_dict.items():
        temp_result_dict[field_mapping.get(key, key)] = value
    return temp_result_dict


def del_space(old_str):
    del_rn = old_str.replace('\r\n', '')
    new_str = del_rn.replace('\t', '').strip()
    return new_str