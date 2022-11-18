# encoding: utf-8
# __author:  angel
# date:  2022/11/13
import os
from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium import webdriver
from util.common import get_code
class RegisterPage(BasePage):
    url = "http://www.jpress.cn/user/register"
    user_name = (By.NAME, "username")
    email = (By.NAME, "email")
    first_password = (By.NAME, "pwd")
    confirm_password = (By.NAME, "confirmPwd")
    captcha_img = (By.XPATH, '//*[@id="captchaimg"]')
    captcha_input = (By.NAME, "captcha")
    agree = (By.ID, "agree")
    submit = (By.XPATH, "/html/body/main/div/div/form/div[7]/button")

    def __init__(self, driver):
        super().__init__(driver)

    def get_url(self):
        self.open_url(self.url)


    def input_name(self, username):
        self.clear(*self.user_name)
        self.input_text(username, *self.user_name)

    def input_email(self, email):
        self.clear(*self.email)
        self.input_text(email, *self.email)

    def first_pwd_input(self, first_pwd):
        self.clear(*self.first_password)
        self.input_text(first_pwd, *self.first_password)

    def confirm_pwd(self, confirm_pwd):
        self.clear(*self.confirm_password)
        self.input_text(confirm_pwd, *self.confirm_password)

    def get_img_code(self):
        img_path = os.path.dirname(os.path.abspath(__file__)) + "/code.img"
        self.screenshot(img_path, *self.captcha_img)
        code = get_code(img_path)
        return code


