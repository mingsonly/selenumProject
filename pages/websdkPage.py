
# encoding: utf-8
import time
import allure
from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium import webdriver

@allure.story("websdk登录")
class WebSDKPage(BasePage):
    url = "https://uat-cloud.hongwuniu.com/page/gsdk/demo/index.html?appkey=5551_PC_42&secret=$2a$10$nf6bHoHaY6GsfvplrQZqde.H.q.IbHR.9msI1Qv5Zi8QerbZxyfC2&env=dev"
    connect_loc = (By.ID, "connect")
    run_loc = (By.ID, "run")
    busyOpt_loc = (By.ID, "funcSelect")
    userID_loc = (By.ID, "tenant_account")
    userToken_loc = (By.ID, "tenant_token")
    userEnv_loc = (By.ID, "envData")
    authEnv_loc = (By.ID, "tenant_authServer")
    app_key_loc = (By.ID, "app_key")
    app_cert_loc = (By.ID, "app_setcert")
    otherParams_loc = (By.ID, "tenant_params")
    ssl_loc = (By.ID, "sslSelect")
    login_loc = (By.ID, "login")

    def __int__(self, webdriver):
        super().__init__(webdriver)

    @allure.step("打开环境地址")
    def open_env(self):
        self.open_url(self.url)

    @allure.step("链接服务")
    def connect_server(self):
        self.click(self.connect_loc)

    @allure.step("输入用户id")
    def input_userId(self, userId):
        self.clear(self.userID_loc)
        self.input_text(userId, self.userID_loc)

    @allure.step("输入token")
    def input_token(self, token):
        self.clear(self.userToken_loc)
        self.input_text(token, self.userToken_loc)

    @allure.step("输入env")
    def input_env(self, env):
        self.clear(self.userEnv_loc)
        self.input_text(env, self.userEnv_loc)

    @allure.step("输入认证环境")
    def input_auth_env(self, env):
        self.clear(self.authEnv_loc)
        self.input_text(env, self.authEnv_loc)

    @allure.step("输入appkey")
    def input_appkey(self, appkey):
        self.clear(self.app_key_loc)
        self.input_text(appkey, self.app_key_loc)

    @allure.step("输入appsert")
    def input_appsert(self, appsert):
        self.clear(self.app_cert_loc)
        self.input_text(appsert, self.app_cert_loc)

    @allure.step("输入其他参数")
    def input_others_params(self, other_params):
        self.clear(self.otherParams_loc)
        self.input_text(other_params, self.otherParams_loc)

    @allure.step("启用ssl")
    def enable_ssl(self, value="use"):
        """
        是否使用ssl登录
        :param value: use or none
        :return: None
        """
        self.select_option(self.ssl_loc, value)

    @allure.step("不使用ssl")
    def unable_ssl(self, value="none"):
        """
        是否使用ssl登录
        :param value: use or none
        :return: None
        """
        self.select_option(self.ssl_loc, value)

    @allure.step("登录")
    def login(self):
        self.click(self.login_loc)

    @allure.step("关闭浏览器")
    def close(self):
        self.quit()

    @allure.step("执行js命令")
    def exec_js_cmd(self, cmd):
        self.exex_js(cmd)
