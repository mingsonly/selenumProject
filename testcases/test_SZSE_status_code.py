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
from util.common import fetch_code, execute_cmd_commind,str_to_timeStamp

logger = get_logger()
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")
data_dir = os.path.join(os.path.dirname(cur_dir), "data")


class TestAndroidSDK:
    def setup(self):
        # todo 切记 这里链接得是模拟器，如果电脑插上其他手机在充电，会默认发送到充电得实体机器上。
        # 连接夜神模拟器
        execute_cmd_commind(cmd='adb_connect_nox')
        caps = {}
        caps["platformName"] = "android"
        caps["appium:deviceName"] = "005da3360804"
        caps["appium:appPackage"] = "com.org.test"
        caps["appium:appActivity"] = ".MainActivity"
        caps["appium:autoGrantPermissions"] = True
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        # caps["appium:newCommandTimeout"] = 3600
        # caps["appium:connectHardwareKeyboard"] = True
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

        self.androidPage = AndBasePage(driver)
        self.envs = self.get_sdk_cfg()['envs']
        self.androidPage.imp_wait(1)
        self.status_code = {
            "1002001000": '{"message":"登录成功,行情已开启","code":1002001000}',
            "1002001001": '{"message":"主行情连接正常关闭","code":1002001001}',
        }
        # 获取case开始执行得时间，目的用于校验抓取得日志在执行得这段时间内得
        self.log_startTS = int(time.time())

    def setup_class(self):
        pass

    def teardown(self):
        self.androidPage.quit()
        # pass

    def teardown_class(self):
        pass

    def get_sdk_cfg(self):
        web_sdk_cf = os.path.join(data_dir, "web_sdk.json")
        with open(web_sdk_cf, "r") as f:
            data = json.load(f)
        return data

    def driver_config(self):
        caps = {}
        caps["platformName"] = "android"
        caps["appium:deviceName"] = "005da3360804"
        caps["appium:appPackage"] = "com.org.test"
        caps["appium:appActivity"] = ".MainActivity"
        caps["appium:autoGrantPermissions"] = True
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        # caps["appium:newCommandTimeout"] = 3600
        # caps["appium:connectHardwareKeyboard"] = True
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
        return driver

    def sdk_login(self):
        # userid, token, loginAppKey, appSecret, env = 123121231, 2313121, "778_Mobile_34", "$2a$10$PT8Nig9yoNyJAqOBXbsKwuDNTC2HIaoOqQrQhQEcF9eOFWWZR.C8q", "uat"
        userid, token, loginAppKey, appSecret, env = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6", "uat"
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(1)
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env=env)

    # todo 存在 appium版本兼容问题
    def test_status_code_1002001000(self):
        """1002001000：建立行情连接成功"""
        execute_cmd_commind(cmd='adb_logcat')
        self.sdk_login()
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        code = self.status_code["1002001000"]
        result = fetch_code(code, self.log_startTS)
        assert result

    def test_status_code_1002001001(self):
        """1002001001：断开行情连接成功"""
        self.sdk_login()
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.androidPage.disconnect()
        time.sleep(10)
        # self.androidPage.imp_wait(5)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        code = self.status_code["1002001001"]
        result = fetch_code(code, self.log_startTS)
        assert result


    def test_status_code_1002001002(self):
        """1002001002：行情连接断开，正在尝试重连"""
        self.sdk_login()
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        # 1-飞行模式，2-wify,3-数据
        self.androidPage.internetOff(1)
        time.sleep(10)
        # self.androidPage.imp_wait(5)
        self.androidPage.internetOff(2)
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001002"
        result = fetch_code(code, self.log_startTS)
        assert result
