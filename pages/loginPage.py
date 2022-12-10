# encoding: utf-8
# __author:  angel
# date:  2022/11/18
from pages.basepage import BasePage
from selenium.webdriver.common.by import By
import allure
import time


@allure.feature("登陆页面")
class LoginPage(BasePage):
    url = "https://uat-adminsdk.hongwuniu.com/#/login"
    userName_loc = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/div[1]/div/div/input')
    password_loc = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/div[2]/div/div/input')
    remember_loc = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/div[3]/label/span[2]')
    login_loc = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/button')


    def __init__(self, webdiver):
        super(LoginPage, self).__init__(webdiver)

    @allure.step("打开登陆页地址")
    def get_url(self):
        self.open_url(self.url)

    @allure.step("输入用户名")
    def input_username(self, phone):
        self.clear(self.userName_loc)
        self.input_text(phone, self.userName_loc)

    @allure.step("输入密码")
    def input_pwd(self, pwd):
        self.clear(self.password_loc)
        self.input_text(pwd, self.password_loc)

    @allure.step("记住我")
    def remember_me(self):
        self.click(self.remember_loc)

    @allure.step("点击登陆")
    def login(self):
        self.click(self.login_loc)

    @allure.step("获取登陆后用户名")
    def get_username(self):
        user_name = self.get_element(self.userName_loc).text
        return user_name

    # @allure.step("错误的密码")
    # def get_password_error(self):
    #     pwd_err_msg = self.get_element(self.pwd_err_loc).text
    #     png_name = "password_err_" + str(time.time()).split('.')[1] + ".png"
    #     self.screenshot_and_save(file_name=png_name)
    #     return pwd_err_msg
    #
    # @allure.step("错误的手机号")
    # def get_phone_error(self):
    #     phone_err_msg = self.get_element(self.phone_err_loc).text
    #     png_name = "phone_err_" + str(time.time()).split('.')[1] + ".png"
    #     self.screenshot_and_save(file_name=png_name)
    #     return phone_err_msg
