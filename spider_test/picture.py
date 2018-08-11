import re
import urllib.request
from urllib import parse


def main(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)
    return res.read().decode()


def get_num(html):
    num = re.findall('<em>(\d*)</em>', html)
    if num:
        return num
    else:
        return 0


def get_company_name(html):
    company = re.findall('<a .* target="_blank">(.*公司|.*学校)</a>', html)
    return company


def get_area(html):
    areas = re.findall('<div class="search_newlist_topmain1 fl" style="width:710px;height:34px"><a href="/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&sm=0&isfilter=1&p=1" class="xzbold fl">()</a>')
    return areas


def get_pay(html):
    pay = re.findall('<td class="zwyx">(\d*-\d*)</td>|面议', html)
    return pay


if __name__ == '__main__':
    city = input('请输入城市')
    job = input('请输入岗位')
    search = parse.urlencode({'jl': city, 'kw': job})
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=python'
    companys = get_company_name(main(url))
    for i in range(len(companys)+1):
        print(companys[i], get_pay(main(url))[i])
        print()

