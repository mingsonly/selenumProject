# encoding: utf-8
# __author:  angel
# date:  2022/11/13

from selenium import webdriver

from exec.myexe import ElementNotFound
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import Select
import time

cur_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")


class BasePage(object):
    _blacklist = [
        (By.ID, "image_cancel"),
        (By.ID, "tips")
    ]

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.max_window()

    def open_url(self, url):
        self.driver.get(url)

    def get_element(self, loc):
        # loc=(by=By.ID,value="")
        time.sleep(1)
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

    def screenshot_ele(self, loc, path=""):
        """获取指定元素截图
        :param path:/dir/x.img or x.png
        :return None
        """
        path = os.path.join(img_dir, loc[1] + ".png") if path == "" else path
        self.get_element(loc).screenshot(path)

    def select_option(self, loc, value):
        se = self.get_element(loc)
        select = Select(se)
        time.sleep(2)
        select.select_by_value(value)

    def screenshot_and_save(self, file_name):
        import time
        file_name = file_name if file_name else str(time.time()) + ".png"
        path = os.path.join(img_dir, file_name)
        self.driver.get_screenshot_as_file(path)

    def quit(self):
        self.driver.quit()

    def click(self, loc):
        self.get_element(loc).click()

    def max_window(self):
        self.driver.maximize_window()

    def exex_js(self, js):
        self.driver.execute_script(js)
