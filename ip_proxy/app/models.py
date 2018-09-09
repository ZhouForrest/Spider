import pyssdb


class SsdbModel(object):

    def __init__(self):
        self.host = '10.28.100.151'
        self.port = 8888
        # self.client = pyssdb.Client(host=self.host, port=self.port)
        # self.client = pyssdb.ConnectionPool(host=self.host, port=self.port)
        self.client = ''
    def get_fast_proxy(self):
        """
        获取代理延迟小于300ms的代理
        :return:
        """
        return self.client.keys('0_', '0_~', 10000)

    def get_yun_proxy(self):
        """
        获取代理云
        :return:
        """
        return self.client.keys('1_', '1_~', 10000)

    def get_owner_proxy(self):
        """
        获取自建代理
        :return:
        """
        return self.client.keys('2_', '2_~', 10000)

    def get_other_proxy(self):
        """
        获取其他代理
        :return:
        """
        return self.client.keys('3_', '3_~', 10000)

    def get_back_proxy(self):
        """
        获取黑名单
        :return:
        """
        return self.client.keys('b_', 'b_~', 1000000)

    def get_ttl(self, ip):
        return str(self.client.ttl(ip))[2:-1]

    def get_ip(self, msg):
        return self.client.keys('msg', 'msg~', 1000000)

    def to_dict(self, base):
        base_ip = str(base)[2:-2]
        port = base_ip.split(':')[1]
        ip = base_ip.split(':')[0].split('_')[1]
        return {
            'ip': ip,
            'port': port,
        }



