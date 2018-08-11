import urllib
from lxml import etree
import requests


def get_msg():
    i = 0
    while i < 10:
        url = 'https://www.kuaidaili.com/free/intr/%s/' % i
        write_ip_msg(url)
        i += 1


def write_ip_msg(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    html = etree.HTML(req.content.decode('utf-8'))
    results = html.xpath('//*[@id="list"]/table/tbody/tr')
    for res in results:
        ip = res.xpath('./td[1]/text()')
        port = res.xpath('./td[2]/text()')
        proxy_url = {'http': 'http://%s:%s' % (ip[0].strip(), port[0].strip())}
        # 代理设置
        Url = 'https://www.baidu.com'
        try:
            response = requests.get(Url, headers=headers, proxies=proxy_url)
            if response.content:
                with open('ip_msg.text', 'a') as f:
                    f.write(ip[0].strip()+':'+port[0].strip()+"\n")
        except:
            print('无效ip')


if __name__ == '__main__':
    get_msg()