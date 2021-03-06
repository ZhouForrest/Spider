from scrapy.spider import Spider, Request
from scrapy import Selector


class Crawel__qyxg_xzxk__credit_changchun(Spider):
    name = 'Crawel__qyxg_xzxk__credit_changchun'
    start_urls = ['http://cccredit.changchun.gov.cn/web/dou/permit/non/list']
    base_url = 'http://cccredit.changchun.gov.cn'
    field_mapping = {
        '行政许可决定书文号': 'license_code',
        '项目名称': 'case_name',
        '审批类别': 'approval_category',
        '许可内容': 'license_content',
        '行政相对人名称': 'company_name',
        '行政相对人代码_1(统一社会信用代码)': 'credit_code',
        '行政相对人代码_2(组织机构代码)': 'organization_code',
        '行政相对人代码_3(工商登记码)': 'regno',
        '行政相对人代码_4(税务登记号)': 'tax_code',
        '行政相对人代码_5(居民身份证号)': 'id_number',
        '法定代表人姓名': 'Frname',
        '许可决定日期': 'license_start_date',
        '许可截止期': 'license_end_date',
        '许可机关': 'license_org',
        '当前状态': 'license_status',
        '地方编码': 'administrative_code',
        '数据更新时间戳': 'update',
        '备注': 'remark'
    }
    def parse(self, response):
        res = Selector(response)
        totalcount = res.xpath('/html/body/div/div[3]/@totalcount').extract()[0]
        totalpage = int(int(totalcount) / 15 + 1)
        for i in range(1, totalpage + 1):
            url = response.url + '?page.pageNo=' + str(i)
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        res = Selector(response)
        info_list = res.xpath('/html/body/div/table/tr')[1:]
        for info in info_list:
            url = self.base_url + info.xpath('./td[1]/a/@href').extract()[0]
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        res = Selector(response)
        info_list = res.xpath('/html/body/div[2]/div/div[2]/div[2]/table/tr')
        res_dict = {}
        for info in info_list:
            key = info.xpath('./th/text()').extract()[0]
            value = info.xpath('./td/text()').extract()[0] if info.xpath('./td/text()') != [] else ''
            res_dict[key] = value
        return self.map_field(res_dict)


    def map_field(self, result_dict):
        if not isinstance(result_dict, dict):
            raise TypeError('except a dict to map the field')
        temp_result_dict = {}
        for key, value in result_dict.items():
            temp_result_dict[self.field_mapping.get(key, key)] = value
        return temp_result_dict