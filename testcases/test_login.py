# encoding: utf-8
# __author:  angel
# date:  2022/11/18
from selenium import webdriver
from pages.loginPage import LoginPage
import time
from selenium.webdriver import ActionChains
import pytest


class TestLogin:
    def setup(self):
        self.driver = webdriver.Chrome()
        self.loginPage = LoginPage(self.driver)

    def setup_class(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        pass

    @pytest.mark.parametrize("phone,pwd", [
        ("17521787146", "taoming123"),
    ])
    def test_login(self, phone, pwd):
        self.loginPage.get_url()
        self.loginPage.input_phone(phone)
        self.loginPage.input_pwd(pwd)
        self.loginPage.agreement()
        self.loginPage.login()
        time.sleep(10)
        user_name = self.loginPage.get_userName()
        assert user_name == 'Geek_cd8e8c'
