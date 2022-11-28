# encoding: utf-8
# __author:  angel
# date:  2022/11/13

from selenium import webdriver

from exec.myexe import ElementNotFound
from selenium.webdriver.common.by import By


class BasePage(object):
    _blacklist = [
        (By.ID, "image_cancel"),
        (By.ID, "tips")
    ]

    def __init__(self, driver: webdriver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def get_element(self, loc):
        # loc=(by=By.ID,value="")
        try:
            element = self.driver.find_element(*loc)
        except ElementNotFound:
            self.handle_exception()
            element = self.driver.find_element(*loc)
        return element

    def handle_exception(self):
        for locator in self._blacklist:
            page_source = self.driver.page_source
            if locator in page_source:
                self.driver.find_element(*locator).click()

    def input_text(self, text, loc):
        self.get_element(loc).send_keys(text)

    def input_and_click(self, loc):
        self.get_element(loc).click()

    def clear(self, loc):
        self.get_element(loc).clear()

    def get_title(self):
        return self.driver.title

    def screenshot(self, path, loc):
        """获取指定元素截图
        :param path:/dir/x.img or x.png
        :return None
        """
        self.get_element(loc).screenshot(path)

    def quit(self):
        self.driver.quit()

    def click(self, loc):
        self.get_element(loc).click()