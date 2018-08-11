from random import randint
from urllib import parse

from bs4 import BeautifulSoup
import threading

import requests
import json


def main(url):
    herders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    timeout = randint(5, 15)
    res = requests.get(url, headers=herders, timeout=timeout)
    results = res.json()
    return results


def get_movie_msg(movie_urls):
    herders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    timeout = randint(5, 15)
    movie_url = movie_urls.pop()
    res = requests.get(movie_url, headers=herders, timeout=timeout)
    soup = BeautifulSoup(res.content.decode('utf-8'), 'lxml')
    movie_results = soup.find_all('p')[0].text

    return json.loads(movie_results)


class MyThread(threading.Thread):
    def __init__(self, movie_urls):
        super(MyThread, self).__init__()
        self.movie_urls = movie_urls

    def get_movie(self):
        return self.re

    def run(self):
        global lock
        lock.acquire()
        re = get_movie_msg(self.movie_urls)
        lock.release()
        self.re = re


def get_movie_url(results):
    movie_base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=0'
    movie_urls = []
    for result in results['tags']:
        search = parse.urlencode({'tag': result})
        movie_url = movie_base_url % search
        movie_urls.append(movie_url)
        return movie_urls


if __name__ == '__main__':
    url = 'https://movie.douban.com/j/search_tags?type=movie&source='
    movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=0'
    results = main(url)
    movie_urls = get_movie_url(results)
    t1 = MyThread(movie_urls)
    t2 = MyThread(movie_urls)
    while True:
        if movie_urls:
            t1.start()
            t2.start()
        else:
            break
    result = t1.get_movie()['subjects']
    movie_msg = []
    for msg in result:
        title = msg['title']
        rate = msg['rate']
        movie_msg.append([title, rate])
    print(movie_msg)



