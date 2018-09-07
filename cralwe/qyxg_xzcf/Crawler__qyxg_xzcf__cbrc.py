# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      Crawler__qyxg_xzcf__cbrc.py
    Description:    银监会-行政处罚
    Author:         Jack Deng
    Date:           2017-09-18
    version:        v.1.0
-------------------------------------------------
"""
import copy
import json
import re
import traceback
import uuid

from scrapy import Request

from hive_framework_milk.commons.utils.selector_util import clean_all_space
from hive_framework_milk.scrapy_spiders.spiders.spider_all import SpiderAll
from hive_worker_hot_coffee.scrapy_spiders.specific_spiders.qyxg_xzxk.field_mapping import map_field


class Crawler__qyxg_xzcf__cbrc(SpiderAll):
    """
    银监会-行政处罚
    """

    name = "Crawler__qyxg_xzcf__cbrc"
    start_urls = ["http://www.cbrc.gov.cn/forwardToXZCFPage2.html"]

    def custom_init(self, *args, **kwargs):
        self.which_one = [
            "银监会机关", "银监局", "银监分局"
        ]

    def parse(self, response):
        """
        get three more href to yield
        :param response:
        :return:
        """
        try:
            more_hrefs = response.xpath('//a[contains(., "更多")]/@href').extract()
            for index, href in enumerate(more_hrefs):
                # if index == 0: #debug
                url = response.urljoin(href)
                yield Request(
                    url=url,
                    dont_filter=True,
                    callback=self.get_pages,
                    errback=self.err_parse,
                    meta={'which' : self.which_one[index]}
                )
                self.logger.info("yield List reqeust url: {} which: {}".format(url, self.which_one[index]))
                # break # debug
        except Exception as err:
            self.logger.error(
                msg="Exception occurred on parsing for first page[{url}]:{error} trace{tb}".format(url=response.url,
                                                                                            error=err,
                                                                                            tb=traceback.format_exc()),
                )


    def get_pages(self, response):
        """
        get page numbers
        :param response:
        :return:
        """
        try:
            which = response.meta['which']
            for req in self.parse_list(response):
                yield req
            pages_count = int(re.search(r'请输入小于(\d+).*?', response.text).group(1))
            for page in range(2, pages_count + 1):
                if which == "银监会机关":
                    url = "".join([response.url.replace('.html', ''), "&current=", str(page)])
                else:
                    url = "".join([response.url, "?current=", str(page)])
                yield Request(
                    url=url,
                    dont_filter=True,
                    callback=self.parse_list,
                    errback=self.err_get_pages,
                    meta={'which' : which, 'page' : str(page)}
                )
                self.logger.info("yield {} page {} to get detail url".format(which, page))
        except Exception as err:
            self.logger.error(
                msg="Exception occurred on parsing for first page[{url}]:{error} trace{tb}".format(url=response.url,
                                                                                            error=err,
                                                                                            tb=traceback.format_exc()),
                )

    def parse_list(self, response):
        """
        parse one page to yield each detail url
        :param response:
        :return:
        """
        try:
            which = response.meta['which']
            try:
                page = response.meta['page']
            except:
                page = "1"
            trs = response.xpath('//div[@class="xia3"]//tr')
            hrefs = ["".join(td.xpath('.//a/@href').extract()) for td in trs.xpath('.//td[position()=1]')]
            titles = ["".join(td.xpath('.//a/@title').extract()) for td in trs.xpath('.//td[position()=1]')]
            pubdates = [clean_all_space(td.xpath('string(.)').extract()) for td in trs.xpath('.//td[last()]')]
            hrefs_pubs_titles = zip(hrefs[0:-1], pubdates[0:-1], titles[0:-1]) #
            for href, pubdate, title in hrefs_pubs_titles:
                url = response.urljoin(href)
                if "报告" in title or "公告" in title or "目录" in title:
                    self.logger.warning("{} page {} url {} is unrelated, wont crawl".format(
                        which, page, url
                    ))
                    continue
                yield Request(
                    url=url,
                    callback=self.parse_detail,
                    errback=self.err_list,
                    meta={'which' : which, 'page' : page, 'public_date' : pubdate, 'title' : title}
                )
                self.logger.info("yield {} page {} detail url {}".format(
                    which, page, url
                ))

            # yield Request(  # bugfix test
            #     url="http://www.cbrc.gov.cn/chinese/home/docView/CFEDE60A320448CAA3FD920B1F7A1357.html",
            #     callback=self.parse_detail,
            #     errback=self.err_list,
            #     meta={'which': "银监局", 'page': 0, 'public_date': "2016-03-24", 'title': "宁波银监局行政处罚信息公开表"}
            # )
        except Exception as err:
            self.logger.error(
                msg="Exception occurred on parsing for first page[{url}]:{error} trace{tb}".format(url=response.url,
                                                                                            error=err,
                                                                                            tb=traceback.format_exc()),
                )

    def parse_detail(self, response):
        """
        parse detail
        :param response:
        :return:
        """
        try:
            which = response.meta['which']
            page = response.meta['page']
            part_res = {
                "public_date" : response.meta['public_date'],
                "title" : response.meta['title']
            }
            if "附件信息" in response.text:
                self.logger.warning("{} page {} url {} is just a .pdf link, wont parse".format(
                    which, page, response.url
                ))
                return
            section1 = response.xpath('//div[@class="WordSection1"]')
            if not section1:
                section1 = response.xpath('//div[contains(@class, "Section")]')
            if not section1:
                raise Exception("{} page {} url {} get data failed, please check it out!".format(
                    which, page, response.url
                ))
            tables = section1.xpath('.//table[@class="MsoNormalTable"]')
            if not tables:
                tables = section1.xpath('.//table[@class="MsoTableGrid"]')
            if tables:
                for item in self.deal_tables(tables, part_res, response):
                    yield item
            else:
                for item in self.deal_main(section1, part_res, response):
                    yield item

        except Exception as err:
            self.logger.error(
                msg="Exception occurred on parsing for first page[{url}]:{error} trace{tb}".format(url=response.url,
                                                                                            error=err,
                                                                                            tb=traceback.format_exc()),
                )

    def deal_main(self, main_html, result, response):
        """
        catch main text
        :param main_html:
        :param result:
        :param response:
        :return:
        """
        try:
            item = self.result_item_assembler(response)
            item['bbd_html'] = ''
            punish_org_text = "".join(main_html.xpath('.//p[contains(., "监管局") and contains(., "中国")]').xpath('string(.)').extract())
            punish_org = re.search(r'(中国.*?监管局).*?', punish_org_text).group(1) if punish_org_text else ""
            punish_code = "".join(main_html.xpath('//p[contains(., "监罚")]').xpath('string(.)').extract())
            if response.meta['which'] != "银监会机关":  # dont parse province for 银监会机关
                province_text = "".join(
                    main_html.xpath('//div[@id="docTitle"]/div[contains(., "文章来源")]/text()').extract())
                province = re.search(r'文章来源.*?([\u4e00-\u9fa5]{2})', province_text).group(1)
            else:
                province = ""
            main = "".join(main_html.xpath('.//p[contains(., "监罚")]//following-sibling::*').extract())
            if not main:
                main = "".join(main_html.xpath('.//*').extract())
            result.update({
                "punish_code" : punish_code,
                "province" : province,
                "main" : main,
                "punish_org" : punish_org
            })
            item['_parsed_data'] = result
            yield item
            self.logger.info("parse main successed, {} page {} url {} data {}".format(
                response.meta['which'], response.meta['page'], response.url, json.dumps(result)
            ))
        except:
            self.logger.error("error on deal_tables {} trace {}".format(
                response.url, traceback.format_exc(),
            ))

            
    def deal_tables(self, tables, result, response):
        """
        parse table
        :param tables:
        :param result:
        :param response:
        :return:
        """
        try:
            item = self.result_item_assembler(response)
            item['bbd_html'] = ''
            punish_code_num = len(re.findall(r'(行政处罚决定书文号|处罚决定书文号)', response.text))
            if response.meta['which'] != "银监会机关":  # dont parse province for 银监会机关
                province_text = "".join(
                    response.xpath('//div[@id="docTitle"]/div[contains(., "文章来源")]/text()').extract())
                province = re.search(r'文章来源.*?([\u4e00-\u9fa5]{2})', province_text).group(1)
            else:
                province = ""
            result.update({'province' : province})
            if punish_code_num == 1 and len(tables) == 3:
                # 处理　"银监分局" 里的特殊情况
                trs = tables.xpath('.//tr')
                titles, values = [], []
                for tr in trs:
                    tds = tr.xpath('.//td')
                    if len(tds) == 1:
                        continue
                    # http://www.cbrc.gov.cn/chinese/home/docView/7E4321407D13435D99064AA007A538B7.html
                    titles.append(clean_all_space(tds[len(tds) - 2].xpath('string(.)').extract()))
                    values.append("".join(tds[-1].xpath('string(.)').extract()).strip())
                tmp_dict = dict(set(zip(titles, values)))
                tmp_dict.pop("", "")
                maped = map_field(tmp_dict)
                result.update(maped)
                item['_parsed_data'] = result
                yield item
                self.logger.info("parse special table successed, {} page {} url {} data {}".format(
                    response.meta['which'], response.meta['page'], response.url, json.dumps(result)
                ))
            else:
                for table in tables:
                    trs = table.xpath('.//tr')
                    td_firsts = [clean_all_space(td.xpath('string(.)').extract()) for td in trs.xpath('.//td[position()=1]') if
                                 len(trs.xpath('.//td')) > 1]
                    if "序号" in td_firsts:  #  one tr tag, one data
                        #  http://www.cbrc.gov.cn/chinese/home/docView/0C0C87BDA4C3431B925FF7BC2461FA55.html
                        titles = [clean_all_space(td.xpath('string(.)').extract()) \
                                  for td in trs[td_firsts.index("序号")].xpath('.//td')]
                        for tr in trs[td_firsts.index("序号") + 1 : ]:
                            values = ["".join(td.xpath('string(.)').extract()).strip() for td in tr.xpath('.//td')]
                            maped = map_field(dict(zip(titles, values)))
                            maped.pop("序号", "")
                            maped.pop("", "")
                            if re.search(r'[0-9]', maped['punish_date']):
                                punish_date = list(maped.pop('punish_date'))
                                new_punish_date = "{}-{}-{}".format(
                                    "".join(punish_date[:4]),
                                    "".join(punish_date[4:6]),
                                    "".join(punish_date[6:])
                                )
                                maped['punish_date'] = new_punish_date
                            res_dict = copy.deepcopy(result)
                            res_dict.update(maped)
                            new_item = copy.deepcopy(item)
                            new_item['_id'] = "{}".format(uuid.uuid4())
                            new_item['_parsed_data'] = res_dict
                            yield new_item
                            self.logger.info("parse one line one data table successed, {} page {} url {} data {}".format(
                                response.meta['which'], response.meta['page'], response.url, json.dumps(res_dict)
                            ))
                    else:  # title : value in each tr tag
                        titles, values = [], []
                        for tr in trs:
                            tds = tr.xpath('.//td')
                            if len(tds) == 1:
                                continue
                            # http://www.cbrc.gov.cn/chinese/home/docView/D0952CF472AB443486104FB03E6FE862.html
                            titles.append(clean_all_space(tds[len(tds) - 2].xpath('string(.)').extract()))
                            values.append("".join(tds[-1].xpath('string(.)').extract()).strip())

                        if len(titles) == len(values):
                            tmp_dict = dict(zip(titles, values))
                        else:
                            raise Exception('titles ,values get error')
                        tmp_dict.pop("", "")
                        maped = map_field(tmp_dict)
                        if re.search(r'[0-9]', maped['punish_date']) and re.search(r'[年|月|日]', maped['punish_date']):
                            # new_punish_date = maped['punish_date'].replace('年', '-').replace('月', '-').replace('日', '')
                            new_punish_date = "{0}-{1:0>2}-{2:0>2}".format(
                                re.search(r'(\d{4}).*?年', maped['punish_date']).group(1),
                                re.search(r'年.*?(\d{1,2}).*?月', maped['punish_date']).group(1),
                                re.search(r'月.*?(\d{1,2}).*?日', maped['punish_date']).group(1),
                            )
                            maped['punish_date'] = new_punish_date
                        res_dict = copy.deepcopy(result)
                        res_dict.update(maped)
                        new_item = copy.deepcopy(item)
                        new_item['_id'] = "{}".format(uuid.uuid4())
                        new_item['_parsed_data'] = res_dict
                        yield new_item
                        self.logger.info("parse table successed, {} page {} url {} data {}".format(
                            response.meta['which'], response.meta['page'], response.url, json.dumps(res_dict)
                        ))
        except:
            self.logger.error("error on deal_tables {} trace {}".format(
                response.url, traceback.format_exc(),
            ))


    def err_list(self, failure):
        response = failure.value.response
        self.logger.error("Exception occurred on crawling for list page[{url}]:{httpcode}".format(url=response.url,
                                                                                            httpcode=response.status))

    def err_get_pages(self, failure):
        response = failure.value.response
        self.logger.error("Exception occurred on crawling for getpage page[{url}]:{httpcode}".format(url=response.url,
                                                                                            httpcode=response.status))

    def err_parse(self, failure):
        response = failure.value.response
        self.logger.error("Exception occurred on crawling for first page[{url}]:{httpcode}".format(url=response.url,
                                                                                            httpcode=response.status))