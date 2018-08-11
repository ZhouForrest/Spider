from selenium import webdriver

chromedriver = 'c:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get('https://github.com')
driver.find_element_by_css_selector('a[href="/login"]').click()
driver.find_element_by_css_selector('input[name="login"]').send_keys('ZhouForrest')
driver.find_element_by_id('password').send_keys('wsx@1QAZ')
driver.find_element_by_css_selector('input[type="submit"]').click()
# driver.close()关闭当前窗口
driver.quit()#关闭浏览器
