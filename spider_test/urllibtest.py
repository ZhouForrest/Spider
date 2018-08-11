import ssl
import urllib.request
from urllib import parse


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def main(url):
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=header)# 忽略未经审核的ssl认证
    res = urllib.request.urlopen(req)
    print(res.read().decode('utf_8'))


if __name__ == '__main__':
    msg = input('请输入搜索信息:')
    search = parse.urlencode({'wd': msg})
    url = 'https://www.baidu.com/s?%s' % search
    main(url)



