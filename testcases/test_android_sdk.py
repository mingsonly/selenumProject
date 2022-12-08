# coding=utf-8
import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.androidPage import AndBasePage
from util.common import get_logger
import os
import json

logger = get_logger()
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")
data_dir = os.path.join(os.path.dirname(cur_dir), "data")


class TestAndroidSDK:
    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["appium:deviceName"] = "6EJ7N18609022111"
        caps["appium:appPackage"] = "com.org.test"
        caps["appium:appActivity"] = ".MainActivity"
        caps["appium:autoGrantPermissions"] = "true"
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        caps["appium:newCommandTimeout"] = 3600
        caps["appium:connectHardwareKeyboard"] = True

        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
        self.androidPage = AndBasePage(driver)
        self.envs = self.get_sdk_cfg()['envs']
        time.sleep(1)

    def setup_class(self): pass

    def teardown(self):
        self.androidPage.quit()

    def teardown_class(self): pass

    def get_sdk_cfg(self):
        web_sdk_cf = os.path.join(data_dir, "web_sdk.json")
        with open(web_sdk_cf, "r") as f:
            data = json.load(f)
        return data

    def config_env(self):
        driver = self.androidPage
        driver.envs_import_btn()
        time.sleep(1)
        driver.envs_info_input(self.envs)
        time.sleep(1)
        driver.envs_btn_accept()
        time.sleep(2)

    @pytest.mark.parametrize("userid,token,loginAppKey,appSecret,env", [
        (1231231, 23131, "778_Mobile_34", "$2a$10$PT8Nig9yoNyJAqOBXbsKwuDNTC2HIaoOqQrQhQEcF9eOFWWZR.C8q", "uat"),
    ])
    def test_sdk_login(self, userid, token, loginAppKey, appSecret, env):
        self.config_env()
        self.androidPage.connect_click()
        self.androidPage.input_userid(userid=userid)
        self.androidPage.input_token(token=token)
        # self.androidPage.switch_ssl()
        self.androidPage.input_pro_env()
        self.androidPage.input_login_appKey(loginAppKey=loginAppKey)
        self.androidPage.input_login_appSecret(appSecret=appSecret)
        self.androidPage.input_env_editText(env=env)
        # self.androidPage.connect_cancel()
        self.androidPage.connect_submit()

