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
        """打开url"""
        self.driver.get(url)

    def get_element(self, loc):
        """
        获取页面元素，获取不到就进入处理异常函数，然后在重新定位，如果不行就报错。
        :param loc: 元素定位元组
        :return: 该元素对象
        """
        # loc=(by=By.ID,value="")
        time.sleep(1)
        try:
            element = self.driver.find_element(*loc)
        except ElementNotFound:
            self.handle_exception()
            element = self.driver.find_element(*loc)
        return element

    def handle_exception(self):
        """处理异常函数"""
        for locator in self._blacklist:
            page_source = self.driver.page_source
            if locator in page_source:
                self.driver.find_element(*locator).click()

    def input_and_click(self, text, loc):
        """输入文本并点击"""
        self.get_element(loc).send_keys(text)

    def input_text(self, loc):
        """输入文本"""
        self.get_element(loc).click()

    def clear(self, loc):
        """清空动作"""
        self.get_element(loc).clear()

    def get_title(self):
        """获取浏览器标题"""
        return self.driver.title

    def screenshot_ele(self, loc, path=""):
        """获取指定元素截图
        :param path:/dir/x.img or x.png
        :return None
        """
        path = os.path.join(img_dir, loc[1] + ".png") if path == "" else path
        self.get_element(loc).screenshot(path)

    def select_option(self, loc, value):
        """
        业务类型下拉框：根据值定位
        :param loc: 下拉框元素定位
        :param value: 下拉框标签的value值，非下拉框文本
        :return: None
        """
        se = self.get_element(loc)
        select = Select(se)
        time.sleep(2)
        select.select_by_value(value)

    def screenshot_and_save(self, file_name):
        """
        截图并保存，如果文件名参数存在就按照输入的文件名保存，不存在则按照时间戳保存
        :param file_name: 截图的文件名
        :return: None
        """
        import time
        file_name = file_name if file_name else str(time.time()) + ".png"
        path = os.path.join(img_dir, file_name)
        self.driver.get_screenshot_as_file(path)

    def quit(self):
        """
        关闭浏览器
        :return: None
        """
        self.driver.quit()

    def click(self, loc):
        """点击操作"""
        self.get_element(loc).click()

    def max_window(self):
        """最大化窗口"""
        self.driver.maximize_window()

    def exex_js(self, js):
        """执行js脚本"""
        self.driver.execute_script(js)
