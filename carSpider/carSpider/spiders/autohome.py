import json
import re

from scrapy.spiders import Spider
from scrapy import Selector, Request

from carSpider.items import DealerItem, CarItem, CarConfItem


class AutoHome(Spider):
    name = 'autohome'
    #页面解析城市的接口
    start_urls = ['https://dealer.autohome.com.cn/DealerList/GetAreasAjax?provinceId=0&cityId=510100&brandid=0&manufactoryid=0&seriesid=0&isSales=0', ]
    #按照经销商查找
    mian_urls = 'https://dealer.autohome.com.cn/'
    id = 0

    def parse(self, response):
        res = response.text
        results = json.loads(res)['AreaInfoGroups']
        for a in range(len(results)):
            for v in range(len(results[a]['Values'])):
                citys = results[a]['Values'][v]['Cities']
                for city in citys:
                    area_url = self.mian_urls + city['Pinyin']
                    city_name = city['Name']
                    yield Request(area_url, callback=self.parse_dealer, meta={'city': city_name, 'url': area_url})

    def parse_dealer(self, response):
        res = Selector(response)
        item = DealerItem()
        results = res.xpath('/html/body/div[2]/div[3]/ul/li')
        url = response.meta.get('url')
        city = response.meta.get('city')
        for result in results:
            item['_id'] = self.id
            item['img'] = result.xpath('./a/img/@src').extract()[0]
            item['city'] = city
            item['name'] = result.xpath('./ul/li[1]/a/span/text()').extract()[0]
            item['main_type'] = result.xpath('./ul/li[2]/span/em/text()').extract()[0]
            item['type_num'] = result.xpath('./ul/li[2]/a/text()').extract()[0]
            item['adress'] = result.xpath('ul/li[4]/span[2]/text()').extract()[0]
            main_car_url = result.xpath('./a/@href').extract()[0]
            yield Request('https:' + main_car_url, callback=self.parse_car_msg, meta={'name': item['name'], 'id': item['_id']})
            self.id += 1
            yield item
        total = res.xpath('/html/body/div[2]/div[2]/div[2]/div/span[1]/text()').extract()[0]
        pages = int(total)//15 + 2
        for num in range(2, pages):
            yield Request(url + '/' + '0/0/0/0/'+str(num)+'/1/0/0.html', callback=self.parse_dealer, meta={'url': url, 'city': city})

    def parse_car_msg(self, response):
        res = Selector(response)
        results = res.xpath('//*[@id="cxcx"]/div[2]/div/dl/dd')
        item = CarItem()
        id = response.meta.get('id')
        for result in results:
            cars = result.xpath('.//p[@class="cars"]/a/text()').extract()[0]
            price = result.xpath('.//p[@class="price"]/text()').extract()[0]
            sub_price = result.xpath('.//p[@class="now green"]/text()').extract()[0]
            sell_price = result.xpath('./p[@class="naked red"]/text()').extract()[0]
            total_price = result.xpath('./div/text()').extract()[0].replace('\r\n', '').strip()
            item['id'] = id
            type_url = result.xpath('.//p[@class="cars"]/a/@href').extract()[0]
            item['car_type'] = [
                {'_id': id, 'type': cars, 'price': price, 'sub_price': sub_price, 'sell_price':                       sell_price, 'total_price': total_price}]
            yield Request(self.mian_urls + type_url, callback=self.parse_car_conf, meta={'id': id})
            id += 1
            yield item

    def parse_car_conf(self, response):
        id = response.meta.get('id')
        req = Selector(response)
        res = req.re(r'url:(.*Price.*seriesId.*)')
        conf_urls = res[0].strip().replace('"', '')
        conf_url = self.mian_urls + conf_urls.replace(',', '').split('/', 1)[1]
        yield Request(conf_url, callback=self.prase_car_conf, meta={'id': id})

    def prase_car_conf(self, response):
        res = Selector(response)
        id = response.meta.get('id')
        msg = res.xpath('//*[@id="tab-10"]//div[@class="config-cont"][1]')
        conf_dict = {}
        item = CarConfItem()
        item['id'] = id
        values = msg.xpath('./table/tbody/tr/td/text()').extract()
        keys = msg.xpath('./table/tbody/tr/th/text()').extract()
        for i in range(len(keys)):
            conf_dict[keys[i]] = values[i]
        item['car_conf'] = [conf_dict]
        yield item

















