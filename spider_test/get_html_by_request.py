from bs4 import BeautifulSoup
import requests
from lxml import etree


def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # proxies = {'http': '52.187.162.198:3128'}
    res = requests.get(url, headers=header)
    html = etree.HTML(res.content.decode('utf-8'))
    result = html.xpath('// *[ @ id = "newlist_list_content_table"] / table')
    # // *[ @ id = "newlist_list_content_table"] / table[4] / tbody / tr[1] / td[1] / div / a[1]
    # // *[ @ id = "newlist_list_content_table"] / table[2] / tbody / tr[1] / td[1] / div / a[1]
    # / html / body / div[3] / div[3] / div[3] / form / div[1] / div[1] / div[3] / ul / li[11] / a
    # result[1].xpath('./tr[1] / td[1] / div / a[1]/text() ')[0].replace('\xa0', '')职位
    # result[2].xpath('./tr[1] / td[3] / a[1]/text()')公司名称
    # result[2].xpath('./tr[1] / td[4] /text()')薪资
    # result[2].xpath('./tr[1] / td[5] /text()')工作地点
    return result


    # soup = BeautifulSoup(res.text, 'lxml')
    # results = soup.find_all('a', 'question_link')#查找a标签下属性为question_link元素
    # for result in results:
    #     result.attrs.get('href')


if __name__ == '__main__':
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=python&sm=0&p=1'
    print(get_html(url))




