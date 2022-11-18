# encoding: utf-8
# __author:  angel
# date:  2022/11/18
from selenium import webdriver
from pages.loginPage import LoginPage
import time
from selenium.webdriver import ActionChains
import pytest
from util.common import get_logger

logger = get_logger()


class TestLogin:
    def setup(self):
        self.driver = webdriver.Chrome()
        self.loginPage = LoginPage(self.driver)
        logger.info("测试用户登陆！！")

    def setup_class(self):
        pass

    def teardown(self):
        self.loginPage.quit()

    def teardown_class(self):
        pass

    @pytest.mark.parametrize("phone,pwd", [
        ("17521787146", "taoming123"),
    ])
    def test_login(self, phone, pwd):
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
            assert user_name == 'Geek_cd8e8c'
        except AssertionError as ae:
            logger.error("用户名校验异常", "报错了", exc_info=1)
