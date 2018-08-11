from bs4 import BeautifulSoup
from selenium import webdriver

import requests

cheomed = 'c:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(cheomed)
url = 'https://search.jd.com/Search?keyword=iPhone&enc=utf-8&wq=iPhone&pvid=5be17fbe013546d7a11a2c1936b34baa'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')
phone_img = soup.select('.p-img img')
for img in phone_img:
    img_name = img.attrs.get('src').rsplit('/')[1]
    img_url = 'http:' + img.attrs.get('src')
    response = requests.get(img_url)
    with open('c:/picture' + img_name, 'wb') as f:
        f.write(response.content)