# encoding: utf-8
# __author:  angel
# date:  2022/11/13

# from selenium import webdriver
from appium import webdriver
from exec.myexe import ElementNotFound
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
import os
from selenium.webdriver.support.ui import Select, WebDriverWait
import time

cur_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")


class BasePage(object):
    _blacklist = [
        (By.ID, "image_cancel"),
        (By.ID, "tips"),
        # 授权按钮
        (By.ID, "com.lbe.security.miui:id/permission_allow_foreground_only_button"),
        (By.ID, 'android:id/button1'),
    ]

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']

    def _option_key_event(self, arg, num=0):
        """
        操作实体按键:
        code码 https://developer.android.com/reference/android/view/KeyEvent.html
        :param arg: event_list key
        :param num: KEYCODE_NUM 时用到的对应数字
        :return: None
        """
        event_list = {
            'KEYCODE_HOME': 3,
            'KEYCODE_BACK': 4,
            'KEYCODE_NUM': 8,
            'KEYCODE_MENU': 82,
        }
        if arg == 'KEYCODE_NUM':
            self.driver.press_keycode(8 + int(num))
        elif arg in event_list:
            self.driver.press_keycode(int(event_list[arg]))

    def input_num_by_keyboard(self,num):
        """
        模仿键盘输入数字
        :param num: 数字
        :return: None
        """
        nums = list(num)
        for num in nums:
            self._option_key_event('KEYCODE_NUM',num)


    def swip_down(self, count=1, meth=None):
        """
        向下滑动，下拉框
        :param count: 滑动次数
        :param meth: 传入的方法method(action),如果返回True,则终止刷新
        :return: None
        Examples:
            action.swip_down(count=100,method=lambda action:not action.is_key_text_displayed("暂无元素"))
        """
        if count == 1:
            self.driver.swipe(self.width / 2, self.height * 2 / 5, self.width / 2, self.height * 4 / 5, 2000)
            self.driver.implicitly_wait(1)
        else:
            for x in range(count):
                self.driver.swipe(self.width / 2, self.height * 2 / 5, self.width / 2, self.height * 4 / 5, 2000)
                self.driver.implicitly_wait(1)
                try:
                    if meth(self):
                        break
                except:
                    pass

    def swip_left(self, count=1):
        for x in range(count):
            self.driver.implicitly_wait(1)
            self.driver.swipe(self.width * 9 / 10, self.height / 2, self.width / 10, self.height / 2, 1500)



    def last_back(self):
        self.driver.back()

    def open_url(self, url):
        """打开url"""
        self.driver.get(url)

    def imp_wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    def internet_switch(self, state):
        """网络切换"""
        net_type = {
            1: self.driver.mobile.AIRPLANE_MODE,
            2: self.driver.mobile.WIFI_NETWORK,
            4: self.driver.mobile.DATA_NETWORK,
            6: self.driver.mobile.ALL_NETWORK,
        }
        # 判断当前网络是不是与要设置得一致，不一致就修改

        self.driver.mobile.set_network_connection(net_type[state])

    def wait_util_click(self, loc):
        wait = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(*loc))
        wait.click()

    # todo  这里有问题待调试
    def scroll_web(self, ele_loc):

        from selenium.webdriver import ActionChains

        ele = self.get_element(ele_loc)
        ActionChains(self.driver).scroll_to_element(ele)

        js = 'window.scrollTo(0,document.body.scrollHeight)'
        self.driver.execute_script(js)
        print("23422222222")

    def get_element(self, loc):
        """
        获取页面元素，获取不到就进入处理异常函数，然后在重新定位，如果不行就报错。
        :param loc: 元素定位元组
        :return: 该元素对象
        """
        # loc=(by=By.ID,value="")
        self.imp_wait(2)
        try:
            element = self.driver.find_element(*loc)
        except ElementNotFound:
            self.handle_exception()
            element = self.driver.find_element(*loc)
        return element

    def get_elements(self, loc):
        """
        获取页面元素，获取不到就进入处理异常函数，然后在重新定位，如果不行就报错。
        :param loc: 元素定位元组
        :return: 该元素对象
        """
        # loc=(by=By.ID,value="")
        self.imp_wait(2)
        try:
            elements = self.driver.find_elements(*loc)
        except ElementNotFound:
            self.handle_exception()
            elements = self.driver.find_elements(*loc)
        return elements

    def handle_exception(self):
        """处理异常函数"""
        page_source = self.driver.page_source
        for locator in self._blacklist:
            if locator in page_source:
                self.driver.find_element(*locator).click()

    def input_text(self, text, loc):
        """输入文本并点击"""
        self.clear(loc)
        self.get_element(loc).send_keys(text)

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
