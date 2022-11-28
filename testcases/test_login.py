# encoding: utf-8
# __author:  angel
# date:  2022/11/18
import allure
from selenium import webdriver
from pages.loginPage import LoginPage
import time
from selenium.webdriver import ActionChains
import pytest
from util.common import get_logger,start_webdriver,get_env_data
from exec.myexe import *
import os

logger = get_logger()
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")

@allure.story("用户登陆模块")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, browser, env):
        self.env_data = get_env_data(env)
        self.driver = start_webdriver(browser)
        self.loginPage = LoginPage(self.driver)
        logger.info("测试用户登陆！！")

    def setup_class(self):
        pass

    def teardown(self):
        self.loginPage.quit()

    def teardown_class(self):
        pass

    # @pytest.fixture(autouse=True)
    # def init_driver(self, browser):
    #     browsers = {
    #         "chrome": webdriver.Chrome(),
    #         "firefox": webdriver.Firefox()
    #     }
    #     self.driver = browsers[browser]

    @allure.story("正常登陆案例")
    # @pytest.mark.parametrize("phone,pwd", [
    #     ("17521787146", "taoming123"),
    # ])
    def test_login_success(self):
        phone, pwd = self.env_data['phone'],self.env_data['password']
        self.loginPage.get_url()
        self.loginPage.input_phone(phone)
        logger.debug("输入手机号")
        self.loginPage.input_pwd(pwd)
        logger.debug("输入密码")
        self.loginPage.agreement()
        logger.debug("同意协议")
        self.loginPage.login()
        logger.debug("登陆")
        time.sleep(10)
        user_name = self.loginPage.get_userName()
        try:
            assert user_name is not None
        except AssertionError as ae:
            logger.error("用户名校验异常", "报错了", exc_info=1)

    @allure.story("失败登陆案例")
    @pytest.mark.parametrize("phone,pwd,expect", [
        ("17521787146", "taoming1234", "密码错误"),
        ("1752178714", "taoming123", "请输入正确的手机号"),
    ])
    def test_login_fail(self, phone, pwd,expect):
        self.loginPage.get_url()
        self.loginPage.input_phone(phone)
        logger.debug("输入手机号")
        logger.debug("输入密码")
        self.loginPage.input_pwd(pwd)
        self.loginPage.agreement()
        logger.debug("同意协议")
        self.loginPage.login()
        logger.debug("登陆")
        time.sleep(2)
        real_values = {
            "密码错误": self.loginPage.get_password_error,
            "请输入正确的手机号": self.loginPage.get_phone_error
        }

        assert real_values[expect]() == expect


# if __name__ == '__main__':
#     pytest.main(['--alluredir', './reports', 'test_login.py'])
