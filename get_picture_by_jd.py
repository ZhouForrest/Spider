
import time

import os
from pymongo import MongoClient
import asyncio

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys

chromed = 'c:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(chromed)
driver.get('https://www.jd.com/')
time.sleep(2)
driver.find_element_by_link_text('手机').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="key"]').send_keys('iphone', keys.Keys.ENTER)
time.sleep(5)
index_window = driver.current_window_handle
soup = BeautifulSoup(driver.page_source, 'lxml')
for em in soup.select('.p-name em'):
    phone_type = em.get_text()
    print(phone_type)
for i in soup.select('.p-price i'):
    phone_price = i.get_text()
    print(phone_price)
driver.find_element_by_id('kw').send_keys(keys.Keys.PAGE_DOWN)


class Apple_phone():
    def __init__(self):
        self.url = 'https://www.jd.com/'
        self.chromed = 'c:\chromedriver_win32\chromedriver.exe'
        self.driver = webdriver.Chrome(self.chromed)

    def get_index(self):
        self.driver.get(self.url)
        time.sleep(5)
        self.driver.find_element_by_link_text('手机').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="key"]').send_keys('iphone', keys.Keys.ENTER)

    def next_page(self):
         self.driver.execute_script('window.scrollTo(0, 100000)')
         time.sleep(5)
         self.driver.find_element_by_css_selector('a[class="pn-next"] em').click()

    def get_phone_msg(self):
        self.get_index()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        data = {}
        _id = 0
        for i in range(len(soup.select('.p-name em'))):
            _id += 1
            data['_id'] = _id
            phone_type = soup.select('.p-name em')[i].get_text()
            data['model'] = phone_type
            phone_price = soup.select('.p-price i')[i].get_text()
            data['price'] = phone_price
            phone_img = soup.select('.p-img img')[i].attrs.get('src')
            data['img'] = 'http:' + phone_img
            self.insert_msg_to_db(data)
        for _ in range(100):
            self.next_page()
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            data = {}
            for i in range(len(soup.select('.p-name em'))):
                data['_id'] = _id
                phone_type = soup.select('.p-name em')[i].get_text()
                data['model'] = phone_type
                phone_price = soup.select('.p-price i')[i].get_text()
                data['price'] = phone_price
                phone_img = soup.select('.p-img img')[i].attrs.get('src')
                data['img'] = 'http:' + phone_img
                self.insert_msg_to_db(data)
                _id += 1

    def insert_msg_to_db(self, data):
        conn = MongoClient('mongodb://localhost:27017')
        db = conn.phone
        db.phone.insert(data)

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [self.get_phone_msg()]
        loop.run_until_complete(asyncio.wait(tasks))
        self.driver.quit()


if __name__ == '__main__':
    phone = Apple_phone()
    phone.run()


