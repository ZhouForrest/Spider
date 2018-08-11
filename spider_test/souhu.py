
import re
import urllib.request
import pymysql


def main(url, charsets=('utf-8', 'GBK')):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read()
    html = ''
    for charset in charsets:
        try:
            html = res.decode(charset)
            break
        except:
            print('错误')
    return html


def get_msg(pattern, html):

    patterns = re.compile(pattern, flags=re.S)
    return re.findall(patterns, html)


def write_to_db(data):

    conn = pymysql.connect(host='localhost', port=3306, password=123456, db='sohu', user='root')
    cursor = conn.cursor()
    sql = 'insert into tb_nba_msg values(%s, %s)'
    cursor.executemany(sql, data)
    return '加载成功'


if __name__ == '__main__':
    url = 'http://sports.sohu.com/nba_a.shtml'
    url_pattern = "<a test=a href='(.*?)' target='_blank'>"
    msg_urls = get_msg(url_pattern, main(url))

    data = []
    for msg_url in msg_urls:
        html = main(msg_url)
        title_pattern = "<title>(.*?)</title>"
        content_pattern = "<p>(.*?)</p>"
        msg_title = get_msg(title_pattern, html)
        mgs_content = get_msg(content_pattern, html)
        data.append([msg_title[0], mgs_content[0]])


