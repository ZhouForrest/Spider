import re
from scrapy.spider import Spider, Request
from scrapy import Selector


class Crawel__qyxg_xzxk__credit_taiyuan(Spider):

    name = 'Crawel__qyxg_xzxk__credit_taiyuan'
    start_urls = ['http://www.taiyuan.gov.cn/ztzl/ztzw/xyty/xygs/xzxk/index.shtml']
    base_url = 'http://www.taiyuan.gov.cn'
    page_url = 'http://www.taiyuan.gov.cn/ztzl/ztzw/xyty/xygs/xzxk/index_{}.shtml'
    field_mapping = {
        '企业名称': 'company_name',
        '统一社会信用代码': 'credit_code',
        '等级号证': 'rank_code',
        '项目名称': 'case_name',
        '行政许可决定文号': 'license_code',
        '审批类别': 'approval_category',
        '法定代表人（负责人）姓名': 'frname',
        '许可内容': 'license_content',
        '许可机关': 'license_org',
        '许可生效期': 'license_start_date',
        '许可截止期': 'license_end_date',
        '当前状态': 'license_status',
        '地方编码': 'license_end_date',
        '备注': 'remark',
    }

    def parse(self, response):
        res = Selector(response)
        totalcount = res.xpath('/html/body/script').re('pageCount": .*,')[0]
        pages = int(re.findall('.*(.\d).*', totalcount)[0])
        for i in range(1, pages + 1):
            if i == 1:
                url = response.url
            url = self.page_url.format(str(i))
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        res = Selector(response)
        info_list = res.xpath('//*[@id="List"]/tr')
        for info in info_list:
            url = self.base_url + info.xpath('./td[2]/a/@href').extract()[0]
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        res = Selector(response)
        info_list = res.xpath('/html/body/div[2]/div[2]/table/tbody/tr')
        res_dict = {}
        for info in info_list:
            key = info.xpath('./td[1]/text()').extract()[0]
            value = info.xpath('./td[2]/text()').extract()[0] if info.xpath('./td[2]/text()') != [] else ''
            res_dict[key] = value
        return self.map_field(res_dict)


    def map_field(self, result_dict):
        if not isinstance(result_dict, dict):
            raise TypeError('except a dict to map the field')
        temp_result_dict = {}
        for key, value in result_dict.items():
            temp_result_dict[self.field_mapping.get(key, key)] = value
        return temp_result_dict