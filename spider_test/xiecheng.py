

# def fibo(n):
#     a, b, i = 0, 1, 0
#     while i < n:
#         a, b = b, a + b
#         i += 1
#         print(a, end=',')
#
#
# if __name__ == '__main__':
#     fibo(10)


# l = [1, 2, [3, [4, 5, 6, [7, 8, [9, 10, [11, 12, 13, [14, 15, [16, [17, ]], 19]]]]]]]
#
#
# def search(l):
#     for item in l:
#         if type(item) is list:
#             search(item)
#         else:
#             print(item)
# search(l)

# def counter(n):
#     if n == 0:
#         return 1
#     elif n < 0:
#         return 0
#     else:
#         return counter(n - 2) + counter(n - 3) + counter(n - 1)
#
#
# print(counter(10))

#
# def productor(consumer):
#     next(consumer)
#     n = 0
#     while n < 3:
#         n += 1
#         print('生产%s' % n)
#         r = consumer.send(n)
#         print('消费中%s' % r)
#
#
# def consumer():
#     r = '...'
#     while True:
#         n = yield r
#         if not n:
#             return
#         print('消费%s' % n)
#         r = '消费完'
#
#
# if __name__ == '__main__':
#     consumer = consumer()
#     productor(consumer)


from pymongo import MongoClient
import asyncio
import aiohttp
import json

# conn = MongoClient('mongodb://localhost:27017')
# # conn = MongoClient(host='127.0.0.1', port=27017)
# db = conn.movie
# db.movie.insert({'title': '英雄'})
#
# for movie in db.movie.find():
#     print(movie)


class MovieMsg():
    def __init__(self):
        self.tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
        self.base_movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s'
        self.movie_url = ''
        self.max_page = 10
        self.movie_url = []

    async def get_msg(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.tag_url) as tag_response:
                self.tag_key = self.parse_tag(await tag_response.text())

                for key in self.tag_key:
                    for page in range(self.max_page):
                        movie_url = self.base_movie_url % (key, page*20)
                        async with session.get(movie_url) as movie_response:
                            movie_msg = self.parse_movie(await movie_response.text())
                            data = {}
                            for title in movie_msg['title']:
                                data['title'] = title
                            for rate in movie_msg['rate']:
                                data['rate'] = rate
                            await self.inser_to_db(data)

    def parse_tag(self, response):
        return json.loads(response)['tags']

    def parse_movie(self, response):

        return json.loads(response)['subjects']

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [self.get_msg()]
        loop.run_until_complete(asyncio.wait(tasks))

    async def inser_to_db(self, response):
        conn = MongoClient('mongodb://localhost:27017')
        db = conn.movie
        await db.movie.inser(response)


if __name__ == '__main__':
    movie_msg = MovieMsg()
    movie_msg.run()
