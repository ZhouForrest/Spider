import json

import scrapy
from scrapy import Request



# class WboItem(scrapy.spiders.Spider):
#     name = 'weibo'
#     start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3261134763_-_1042015%253AtagCategory_050&luicode=10000011&lfid=1076033261134763', ]
#
#     def parse(self, response):
#         item = WbspiderItem()
#         msg = json.loads(response.text)
#         users_msg = []
#         for i in range(len(msg['data']['cards'])-1):
#             for users in msg['data']['cards'][i]['card_group'][1]['users']:
#                 users_msg.append(users)
#         for j in range(len(msg['data']['cards'][3]['card_group'])):
#             users_msg.append(msg['data']['cards'][3]['card_group'][j]['user'])
#         _id = []
#         screen_name = []
#         profile_image_url = []
#         profile_url = []
#         followers_count = []
#         follow_count = []
#         cover_image_phone = []
#         for user in users_msg:
#             _id.append(user['id'])
#             screen_name.append(user['screen_name'])
#             profile_image_url.append(user['profile_image_url'])
#             profile_url.append(user['profile_url'])
#             followers_count.append(user['followers_count'])
#             follow_count.append(user['follow_count'])
#             cover_image_phone.append(user['cover_image_phone'])
#
#         item['_id'] = _id
#         item['screen_name'] = screen_name
#         item['profile_image_url'] = profile_image_url
#         item['profile_url'] = profile_url
#         item['followers_count'] = followers_count
#         item['follow_count'] = follow_count
#         item['cover_image_phone'] = cover_image_phone
#         return dict(item)
from wbspider.items import Relation_fans, WbspiderItem, Relation_followers


class WeoBoTtem(scrapy.spiders.Spider):
    name = 'weibo'
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    followers_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    start_users = ['3217179555', '1742566624', '2282991915', '1288739185', '3952070245', '5878659096']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):

        res = json.loads(response.text)
        user_item = WbspiderItem()
        user_pramas = ['screen_name', 'profile_image_url', 'profile_url', 'followers_count', 'follow_count', 'cover_image_phone']
        if res.get('data').get('userInfo'):
            user = res.get('data').get('userInfo')
            user_item['_id'] = user.get('id')
            for k in user_pramas:
                user_item[k] = user[k]
            yield user_item
            yield Request(self.followers_url.format(uid=user_item['_id'], page=1,),               callback=self.parse_follower,
                          meta={'uid': user_item['_id'], 'page': 1})

    def parse_fans(self, response):
        res = json.loads(response.text)
        if res['ok']:
            card_group = res['data']['cards'][-1]['card_group']
            # for card_info in card_group:
            #     user_info = card_info['user']
            #     uid = user_info['id']
            #     yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            relation_fans_item = Relation_fans()
            fans_list = [{'id': card_info['user']['id'], 'screen_name': card_info['user']['screen_name']} for card_info in card_group]
            relation_fans_item['fans'] = fans_list
            yield relation_fans_item
            # 下一页
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.fans_url.format(uid=uid, page=page), callback=self.parse_fans,
                          meta={'uid': uid, 'page': page})

    def parse_follower(self, response):
        res = json.loads(response.text)
        if res['ok']:
            card_group = res['data']['cards'][-1]['card_group']
            for card_info in card_group:
                user_info = card_info['user']
                uid = user_info.get('id')
                yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
        #下一页
            uid = response.meta.get('uid')
            page = response.meta.get('page')+1
            yield Request(self.followers_url.format(uid=uid, page=page),               callback=self.parse_follower,
                          meta={'uid': uid, 'page': page})
            relation_followers_item = Relation_followers()
            followers_list = []
            for card_info in card_group:
                user_info = card_info['user']
                followers_list.append({'id': user_info['id'], 'screen_name': user_info['screen_name']})
                relation_followers_item['followers'] = followers_list
            yield relation_followers_item

