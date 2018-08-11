from bs4 import BeautifulSoup
from selenium import webdriver


chromedriver = 'c:\chromedriver_win32\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get('https://www.taobao.com')
soup = BeautifulSoup(browser.page_source, 'lxml')
# browser.find_element_by_css_selector(".site-nav-sgn a[class='h']").click()
# browser.find_element_by_css_selector(".login-links a[class='forget-pwd']").click()
# browser.find_element_by_css_selector('#TPL-username_1').send_keys('15828550810')
# browser.find_element_by_id('TPL-password_1').send_keys('')
browser.find_element_by_id('q').send_keys('少女')
browser.find_element_by_css_selector('.btn-search[type="submit"]').click()

browser.close()