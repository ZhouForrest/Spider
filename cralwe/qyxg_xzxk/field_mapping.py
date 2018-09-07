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
    "标题": "title",
    "发布时间": "public_date",
    "省份": "province",
    "处罚文号": "punish_code",
    "处罚决定书文号": "punish_code",
    "行政处罚决定文书号": "punish_code",
    "处罚决定文书号": "punish_code",
    "行政处罚决定书文号": "punish_code",
    "编号": "punish_code",
    "处罚问号": "punish_code",
    "姓名": "name",
    "个人姓名": "name",
    "个人名称": "name",
    "被处罚个人姓名": "name",
    "单位": "company_name1",
    "公司名称": "company_name",
    "名称": "company_name",
    "被处罚人姓名或名称": "company_name",
    "被处罚人名称": "company_name",
    "处罚对象": "company_name",
    "被处罚单位名称": "company_name",
    "主要负责人": "frname",
    "法定代表人姓名": "frname",
    "审批类型": "approval_category",
    "法定代表人或主要负责人姓名": "frname",
    "法定代表人（主要负责人）姓名": "frname",
    "法定代表人": "frname",
    "主要负责人姓名": "frname",
    "主要负责人（法定代表人）姓名": "frname",
    "违法事实": "punish_fact",
    "案由": "punish_fact",
    "主要违法违规事实": "punish_fact",
    "主要违法违规事实（案由）": "punish_fact",
    "主要违法事实（案由）": "punish_fact",
    "主要违法事实": "punish_fact",
    "违法违规情况": "punish_fact",
    "主要违法犯罪事实（案由）": "punish_fact",
    "处罚依据": "punish_basis",
    "行政处罚依据": "punish_basis",
    "处罚结果": "punish_content",
    "行政处罚决定": "punish_content",
    "行政处罚种类及金额": "punish_content",
    "行政处罚种类": "punish_content",
    "处罚决定": "punish_content",
    "行政处罚决定内容": "punish_content",
    "处罚机关": "punish_org",
    "作出处罚决定的机关名称": "punish_org",
    "作出处罚的机关": "punish_org",
    "作出行政处罚的机关": "punish_org",
    "作出行政处罚决定的机关名称": "punish_org",
    "作出行政处罚的机关名称": "punish_org",
    "处罚日期": "punish_date",
    "作出处罚决定的日期": "punish_date",
    "作出处罚的日期": "punish_date",
    "作出行政处罚的日期": "punish_date",
    "作出行政处罚决定的日期": "punish_date",
    "时间": "punish_date",
    "履行方式": "perform_way",
    "行政处罚履行方式和期限": "perform_way",
    "正文": "main",
    "索引号": "index_num",
    "分类": "classification",
    "主题词": "keyword",
    "文书号": "punish_code",
    "文号": "punish_code",
    "发布机构": "punish_org",
    "发文日期": "pubdate",
    "项目名称": "case_name",
    "行政许可名称": "case_name",
    "许可项目名称": "case_name",
    "许可名称": "case_name",
    "行政相对人名称": "company_name",
    "被处罚单位（被处罚人）": "company_name",
    "信用主体名称": "company_name",
    "行政相对人": "company_name",
    "主体名称": "company_name",
    "企业名称": "company_name",
    "行政许可决定书文号": "license_code",
    "行政许可决定文书文号": "license_code",
    "行政许可决定文书号": "license_code",
    "许可文号": "license_code",
    "行政许可文号": "license_code",
    "许可文书号": "license_code",
    "许可书文号": "license_code",
    "许可证号": "license_code",
    "许可编号": "license_code",
    "审批类别": "approval_category",
    "许可类型": "approval_category",
    "许可内容": "license_content",
    "行政许可内容": "license_content",
    "统一社会信用代码": "credit_code",
    "代码": "credit_code",
    "代码类型": "credit_type",
    "状态变更日期": "update",
    "行政许可事项名称": "case_name",
    "行政相对人代码_1(统一社会信用代码)": "credit_code",
    "行政相对人代码_1（统一社会信用代码）": "credit_code",
    "行政相对人代码——1（统一社会信用代码）": "credit_code",
    "统一社会信用代码/登记证号": "credit_code",
    "组织机构代码": "organization_code",
    "行政相对人代码_2(组织机构代码)": "organization_code",
    "行政相对人代码_2（组织机构信用代码）": "organization_code",
    "行政相对人代码——2（组织机构代码）": "organization_code",
    "机构代码": "organization_code",
    "工商登记码": "regno",
    "工商注册号": "regno",
    "行政相对人代码_3(工商登记码)": "regno",
    "行政相对人代码_3（工商登记码）": "regno",
    "行政相对人代码——3（工商登记码）": "regno",
    "工商登记号": "regno",
    "企业注册号": "regno",
    "税务登记号": "tax_code",
    "行政相对人代码_4(税务登记号)": "tax_code",
    "行政相对人代码_4（税务登记号）": "tax_code",
    "行政相对人代码——4（税务登记号）": "tax_code",
    "税务登记证号": "tax_code",
    "居民身份证号": "id_number",
    "行政相对人代码_5 (居民身份证号)": "id_number",
    "行政相对人代码_5（居民身份证号）": "id_number",
    "行政相对人代码——5（居民身份证号）": "id_number",
    "居民身份证号码": "id_number",
    "法定代表人（或单位负责人）": "frname",
    "法定代表人、负责人": "frname",
    "法人代表姓名": "frname",
    "许可机关": "license_org",
    "执法部门": "license_org",
    "许可机构": "license_org",
    "许可部门": "license_org",
    "许可生效期": "license_start_date",
    "许可决定日期": "license_start_date",
    "作出行政许可的日期": "license_start_date",
    "许可日期": "license_start_date",
    "有效期起始日期": "license_start_date",
    "许可截止期": "license_end_date",
    "许可截止日期": "license_end_date",
    "有效期截止日期": "license_end_date",
    "许可截至期": "license_end_date",
    "有效期": "license_end_date",
    "当前状态": "license_status",
    "状态": "license_status",
    "行政许可证状态": "license_status",
    "许可状态": "license_status",
    "行政许可状态": "license_status",
    "许可证状态": "license_status",
    "数据更新时间戳": "update",
    "数据时间更新戳": "update",
    "数据更新时间": "update",
    "更新时间": "update",
    "行政区划代码": "administrative_code",
    "地方编码": "administrative_code",
    "备注": "remark",
    "来源单位": "data_source",
    "信息提供部门": "data_source",
    "报送部门": "data_source",
    "公示日期": "pubdate",
    "核发日期": "pubdate",
    "案件名称": "case_name",
    "处罚名称": "case_name",
    "行政处罚决定文书文号": "punish_code",
    "行政处罚决定文书": "punish_code",
    "处罚决定文书编号": "punish_code",
    "处罚文书号": "punish_code",
    "行政处罚文号": "punish_code",
    "处罚事由": "punish_type",
    "处罚内容": "punish_type",
    "违法违规行为": "punish_type",
    "处罚类别": "punish_category_one",
    "处罚类型": "punish_category_one",
    "处罚类别1": "punish_category_one",
    "处罚类型1": "punish_category_one",
    "处罚类别2": "punish_category_two",
    "处罚类型2": "punish_category_two",
    "处理结果": "punish_content",
    "纳税人识别号": "tax_code",
    "行政相对人代码_5(居民身份证号)": "id_number",
    "法定代表人居民身份证号": "id_number",
    "法定代表人身份证号": "id_number",
    "处罚部门": "punish_org",
    "处罚机构": "punish_org",
    "处罚生效期": "public_date",
    "处罚决定日期": "public_date",
    "处罚决定日期（处罚生效期）": "public_date",
    "处罚决定日期(处罚生效期)": "public_date",
    "处罚截止期": "punish_end_date",
    "处罚截至期": "punish_end_date",
    "处罚状态": "punish_status",
    "注册地址": "address",
    "数据报送时间": "pubdate",
    "项目名称": "case_name",
    "主体名称": "company_name",
    "处罚类型": "punish_category_one",
    "公示截止日期": "punish_end_date",
    "行政处罚事项名称": "case_name",
    "许可有效期": "license_last_date",
    "处罚期限": "punish_last_date"
}


def map_field(result_dict):
    if not isinstance(result_dict, dict):
        raise TypeError('except a dict to map the field')
    temp_result_dict = {}
    for key, value in result_dict.items():
        temp_result_dict[field_mapping.get(key, key)] = value
    return temp_result_dict
