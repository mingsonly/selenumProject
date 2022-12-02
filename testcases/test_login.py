# __author:  angel
# date:  2022/11/18
import allure
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.indexPage import IndexPage
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
        self.indexPage = IndexPage(self.driver)
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
        username, pwd = self.env_data['username'], self.env_data['password']
        self.loginPage.get_url()
        self.loginPage.input_username(username)
        logger.debug("输入手机号")
        self.loginPage.input_pwd(pwd)
        logger.debug("输入密码")
        self.loginPage.remember_me()
        logger.debug("同意协议")
        self.loginPage.login()
        logger.debug("登陆")
        time.sleep(5)
        index_title = self.indexPage.get_title()
        assert index_title == '云平台管理系统'

