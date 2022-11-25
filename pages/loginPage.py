# encoding: utf-8
# __author:  angel
# date:  2022/11/18
from pages.basepage import BasePage
from selenium.webdriver.common.by import By
import allure


@allure.feature("登陆页面")
class LoginPage(BasePage):
    phone_loc = (By.NAME, "cellphone")
    pwd_loc = (By.NAME, "password")
    login_btn_loc = (By.CLASS_NAME, "Button_button_3onsJ")
    agree_loc = (By.ID, "agree")
    url = "https://account.geekbang.org/login?redirect=https%3A%2F%2Ftime.geekbang.org%2F"
    pwd_err_loc = (By.CLASS_NAME,"gkui-form-error")

    userName_loc = (By.CLASS_NAME, "user-name")

    def __init__(self, webdiver):
        super(LoginPage, self).__init__(webdiver)

    @allure.step("打开登陆页地址")
    def get_url(self):
        self.open_url(self.url)

    @allure.step("输入手机号")
    def input_phone(self, phone):
        self.clear(*self.phone_loc)
        self.input_text(phone, *self.phone_loc)

    @allure.step("输入密码")
    def input_pwd(self, pwd):
        self.clear(*self.pwd_loc)
        self.input_text(pwd, *self.pwd_loc)

    @allure.step("同意协议")
    def agreement(self):
        self.click(*self.agree_loc)

    @allure.step("点击登陆")
    def login(self):
        self.click(*self.login_btn_loc)

    @allure.step("获取登陆后用户名")
    def get_userName(self):
        user_name = self.get_element(*self.userName_loc).text
        return user_name

    @allure.step("获取密码错误的提示")
    def get_password_error(self):
        pwd_err_msg = self.get_element(*self.pwd_err_loc).text
        return pwd_err_msg
