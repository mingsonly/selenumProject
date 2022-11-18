# encoding: utf-8
# __author:  angel
# date:  2022/11/13

from selenium import webdriver


class BasePage(object):
    def __init__(self, driver:webdriver):
        self.driver = driver

    def open_url(self,url):
        self.driver.get(url)



    def get_element(self, *loc):
        # loc=(by=By.ID,value="")
        element = self.driver.find_element(*loc)
        return element

    def input_text(self, text, *loc):
        self.get_element(*loc).send_keys(text)

    def click(self, *loc):
        self.get_element(*loc).click()

    def clear(self, *loc):
        self.get_element(*loc).clear()

    def get_title(self):
        return self.driver.title

    def screenshot(self, path, *loc):
        self.get_element(*loc).screenshot(path)

    def quit(self):
        self.driver.quit()
