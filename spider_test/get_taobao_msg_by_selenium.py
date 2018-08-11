import time
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.support.ui import Select

chromeDriver = 'c:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(chromeDriver)

driver.get('https://www.jd.com/')
index_window = driver.current_window_handle
html = driver.page_source
# driver.implicitly_wait(5)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="J_cate"]/ul/li[5]/a[2]').click()
# driver.switch_to_window(index_window)
#回退
driver.back()

#前进

# driver.implicitly_wait(5)
time.sleep(10)
driver.find_element_by_xpath('//*[@id="J_cate"]/ul/li[7]/a[3]').click()



# driver.quit()
#搜索 可以根据索引来选择，可以根据值来选择，可以根据文字来选择
# from selenium.webdriver.support.ui import Select
# select = Select(driver.find_element_by_name('name'))
# select.select_by_index('index')
# select.select_by_visible_text("text")
# select.select_by_value('value')

#取消选中
# select = Select(driver.find_element_by_id('id'))
# select.deselect_all()

#元素之间的拖拽
# element = driver.find_element_by_name("source")
# target = driver.find_element_by_name("target")
#
# from selenium.webdriver import ActionChains
#
# action_chains = ActionChains(driver)
# action_chains.drag_and_drop(element, target).perform()
