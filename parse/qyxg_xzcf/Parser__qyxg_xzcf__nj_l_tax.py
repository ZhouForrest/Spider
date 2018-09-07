#!/usr/bin/python3
"""
:Copyright: 2018, BBD Tech. Co.,Ltd.
:File Name: Parser__qyxg_xzcf__nj_l_tax.py
:Author: lvfeng@bbdservice.com
:Date: 2018-06-01 16:35
:Version: v.1.0
:Description: 
"""
import re
from hive_worker_hot_coffee.parsers.manual_parser.qyxg_xzcf.sc_l_tax_base import SC_l_tax_base


class Parser__qyxg_xzcf__nj_l_tax(SC_l_tax_base):
    """内江"""
    key_word_map = {
        '税务处罚决定文书号': 'punish_code',  # gy, 0613
        '行政处罚决定文书号': 'punish_code',
        '行政处罚决定书文号': 'punish_code',
        '政处罚决定文书号': 'punish_code',
        '行政处罚文书号': 'punish_code',
        '行政处罚决定文号': 'punish_code',
        '行政处罚决定书号': 'punish_code',  # ls, 0613
        '行政处罚决定文书': 'punish_code',  # lsz, 0613
    
        '处罚名称': 'case_name',
        '处罚类别': 'punish_category', '处罚类别1': 'punish_category',
        '罚类别': 'punish_category',
        '处罚事由': 'punish_type',
        '处罚是由': 'punish_type',  # lsz 0613
        '罚款事由': 'punish_type',  # lsz 0613
        '处罚依据': 'punish_basis',
        '行政相对人名称': 'company_name', '行政相对人名': 'company_name',
        
        '行政相对人代码': 'credit_code',   # nj, 0613
        '行政相对人代码-1': 'credit_code',
        '行政相对人代码-1（统一社会信用代码）': 'credit_code',
        '行政相对人代码/1（统一社会信用代码）': 'credit_code', '行统一社会信用代码': 'credit_code',
        '统一社会信用代码': 'credit_code',
        '统一社会代码': 'credit_code',
        '行政相对人代码-1（社会统一信用代码）': 'credit_code',
        '行政相对人代码（统一社会信用代码）': 'credit_code', '统一社会信用代': 'credit_code', '行政相对人代码1（统一社会信用代码）': 'credit_code',
        '社会信用代码': 'credit_code',
        '公司 统一社会信用代码': 'credit_code',  # 0613
        '行政相对人代码_1 (统一社会信用代码)': 'credit_code',  # 0613
    
        '行政相对人统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '统一社会信用代码（纳税人识别号）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信用代码）': 'credit_code',  # 需要特殊处理
        '纳税人识别号（统一社会信息代码）': 'credit_code',  # 需要特殊处理，乐山
        '相对人代码': 'credit_code',  # nj, 0620
    
        '行政相对人代码-2（组织机构代码）': 'organization_code',
        '行政相对人代码/2（组织机构代码）': 'organization_code',
        '行政相对人代码-2': 'organization_code',
        '组织机构代码': 'organization_code',  # 0613
        
        '行政相对人代码-3': 'tax_code',
        '行政相对人代码-3（纳税人识别号）': 'tax_code',
        '行政相对人代码/3（纳税人识别号）': 'tax_code',
        '统一社会信用代码（纳税人识别码）': 'tax_code',
        '纳税人识别号': 'tax_code',
        '行政相对人代码（纳税人识别号）': 'tax_code',
    
        '行政相对人代码-4（居民身份证号）': 'id_number',
        '行政相对人代码/4（居民身份证号）': 'id_number',
        '行政相对人代码-4 ': 'id_number',
        '行政相对人代码-4': 'id_number',
    
        '法定代表人姓名': 'frname',
        '法定代表人': 'frname',
        '法人代表': 'frname',  # lsz, 0613
        '处罚结果': 'punish_content',
        '兴处罚决定日期': 'punish_date',
        '处罚决定日期': 'punish_date', '处罚日期': 'punish_date',
        '处罚机关': 'punish_org',
        '当前状态': 'punish_status',
        '当权状态': 'punish_status',
        '地方编码': 'administrative_code',
        '数据更新时间': 'update',
        '数据更新时间戳': 'update',
        '数据更新录入日期': 'update',  # cd, 0613
        '公示期限': 'public_period',
        '备注': 'remark',
    }

    def _get_lines(self, div):
        lines_1 = div.xpath('.//p').xpath('string(.)').extract()
        
        lines_2 = div.xpath('.//p').xpath('string(.)').extract()
        
        lines_3 = div.xpath('.//p').xpath('./text()|./strong/text()').extract()
        
        max_l = (lines_1, len(lines_1))
        for l_ in [(lines_2, len(lines_2)), (lines_3, len(lines_3))]:
            if max_l[1] < l_[1]:
                max_l = l_
        
        return max_l[0]
    
    def _assemble_lines(self, lines):
        _lines = []
        tmp_str = ''
        cur_key = ''
        for l in lines:
            if re.sub('[:：]', '', l) in self.key_word_map:
                if cur_key == '':
                    need_merge = True
                elif cur_key != re.sub('[:：]', '', l):
                    need_merge = False
                else:
                    need_merge = True
                cur_key = re.sub('[:：]', '', l)
            else:
                need_merge = True
            if need_merge:
                tmp_str = tmp_str + l
            else:
                _lines.append(tmp_str)
                tmp_str = l
        _lines.append(tmp_str)
        return _lines if len(lines) > 18 else lines
                
if __name__ == '__main__':
    def _assemble_lines(key_word_map, lines):
        _lines = []
        tmp_str = ''
        cur_key = ''
        for l in lines:
            if re.sub('[:：]', '', l) in key_word_map:
                if cur_key == '':
                    need_merge = True
                elif cur_key != re.sub('[:：]', '', l):
                    need_merge = False
                else:
                    need_merge = True
                cur_key = re.sub('[:：]', '', l)
            else:
                need_merge = True
            if need_merge:
                tmp_str = tmp_str + l
            else:
                _lines.append(tmp_str)
                tmp_str = l
        _lines.append(tmp_str)
        return _lines if _lines else lines
    
    test_lines = ['行政处罚决定文书号', '：资中地税九所简罚〔2018〕41号',
                  '处罚名称', '：税务行政处罚',
                  '处罚类别', '：罚款',
                  '处罚事由', '：未按照规定期限办理纳税申报',
                  '处罚依据', '：《中华人民共和国税收征收管理法》第六十二条',
                  '行政相对人名称', '：资中县吉祥拉丝材料厂（普通合伙）',
                  '相对人代码', '：91511025621052284G',
                  '法定代表人姓名', '：韩沁章',
                  '处罚结果', '：100.00',
                  '处罚决定日期', '：2018年5月25日',
                  '处罚机关', '：四川省资中县地方税务局第九税务所',
                  '当前状态', '：正常',
                  '地方编码', '：641200',
                  '数据更新时间', '：2018年5月25日', '\xa0']
    sn_parser = _assemble_lines(Parser__qyxg_xzcf__nj_l_tax.key_word_map, test_lines)