import requests
from lxml import etree


def main(url):
    herders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get(url)
    results = res.json()
    return results


if __name__ == '__main__':
    url = 'http://mini.eastday.com/json/index/indexMergeNews.json?callback=indexMergeNews&_=1530102513709'
    print(main(url))