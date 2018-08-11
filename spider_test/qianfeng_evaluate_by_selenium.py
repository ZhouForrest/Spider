from selenium import webdriver


class Evaluate(object):
    def __init__(self):
        chromeDriver = 'c:\chromedriver_win32\chromedriver.exe'
        self.driver = webdriver.Chrome(chromeDriver)


if __name__ == '__main__':
    pass
