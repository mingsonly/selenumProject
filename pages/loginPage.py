# encoding: utf-8
# __author:  angel
# date:  2022/11/18
from pages.basepage import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    phone_loc = (By.NAME, "cellphone")
    pwd_loc = (By.NAME, "password")
    login_btn_loc = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div[4]/div")
    agree_loc = (By.ID, "agree")
    url = "https://account.geekbang.org/login?redirect=https%3A%2F%2Ftime.geekbang.org%2F"

    userName_loc = (By.CLASS_NAME, "user-name")

    def __init__(self, webdiver):
        super(LoginPage, self).__init__(webdiver)

    def get_url(self):
        self.open_url(self.url)

    def input_phone(self, phone):
        self.clear(*self.phone_loc)
        self.input_text(phone, *self.phone_loc)

    def input_pwd(self, pwd):
        self.clear(*self.pwd_loc)
        self.input_text(pwd, *self.pwd_loc)

    def agreement(self):
        self.click(*self.agree_loc)

    def login(self):
        self.click(*self.login_btn_loc)

    def get_userName(self):
        user_name = self.get_element(*self.userName_loc).text
        return user_name
