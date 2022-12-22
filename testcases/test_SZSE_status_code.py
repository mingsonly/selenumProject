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
from util.common import fetch_code, execute_cmd_commind, str_to_timeStamp

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
            "1002001000": '{"message":"登录成功,行情已开启","code":1002001000}',  # pass
            "1002001001": '{"message":"主行情连接正常关闭","code":1002001001}',  # pass
            "1002001002": '{"message":"行情连接异常断开,正在重连","code":1002001002}',  # pass
            "1002001003": '{"message":"HTTP网关登录失败，请重新登录","code":1002001003}',  # pass
            "1002001010": '{"message":"行情重连成功","code":1002001010}',  # pass
            "1002001012": '{"message":"HTTP请求异常，正在重试","code":1002001012}',  # pass
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

    def sdk_login(self, env=None):
        # userid, token, loginAppKey, appSecret, env = 123121231, 2313121, "778_Mobile_34", "$2a$10$PT8Nig9yoNyJAqOBXbsKwuDNTC2HIaoOqQrQhQEcF9eOFWWZR.C8q", "uat"
        if env is None:
            env = "uat"
        userid, token, loginAppKey, appSecret = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6"
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(1)
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env=env)
        # 模拟器不需要弹窗
        self.androidPage.phone_permission_enable()

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

    # todo 手动测试通过，自动化和模拟器需要在看看问题
    def test_status_code_1002001002(self):
        """1002001002：行情连接断开，正在尝试重连
        logic: 由于服务端故障、网络中断、客户端休眠等原因导致与行情服务的连接异常断开，SDK会自动进行重连，客户无需处理
        """
        self.sdk_login()
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        # 1-飞行模式，2-wify,3-数据
        self.androidPage.internet_switch(1)
        time.sleep(10)
        # self.androidPage.imp_wait(5)
        # self.androidPage.internet_switch(2)
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001002"
        result = fetch_code(code, self.log_startTS)
        assert result

    def test_status_code_1002001003_invalid_env(self):
        """
        1002001003：建立行情连接失败，无效得环境
        logic: 登录得时候输入无效得环境会触发
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login(env="invalid_env")
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result

    #  todo 半自动化
    def test_status_code_1002001003_platformServer_disconnect(self):
        """
        1002001003：建立行情连接失败，平台登录失败
        logic: 登录后飞行模式--> 切到wify --> 等待20 --> 查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # 1-飞行模式，2-wify,3-数据
        self.androidPage.internet_switch(1)
        time.sleep(10)
        self.androidPage.internet_switch(2)
        time.sleep(20)
        execute_cmd_commind(cmd='adb_close')
        # code = self.status_code["1002001001"]
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result

    #  todo 半自动化
    def test_status_code_1002001003_quotaServer_disconnect(self):
        """
        1002001003：建立行情连接失败，行情服务异常
        logic: 登录后飞行模式--> 切到wify --> 等待20 --> 查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # todo case 挂起，等待运维操作完成，在继续执行
        print("----------")
        time.sleep(20)
        execute_cmd_commind(cmd='adb_close')
        # code = self.status_code["1002001001"]
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 限制登录设备1台，然后多台设备登录同一个账号待处理
    def test_status_code_1002001005(self):
        """
        1002001005：行情服务主动断开与SDK的连接：XXXX
        logic: 由于异常调用或多点登录限制引起的行情服务主动断开连接，该信息主要用于分析断开原因，无需处理
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        userid, token, loginAppKey, appSecret = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6"
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env="uat")
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001005"
        result = fetch_code(code, self.log_startTS)
        assert result

    #  todo 半自动化 待协调验证
    def test_status_code_1002001006(self):
        """
        1002001006：行情连接断开且自动重连失败，请重新登录
        logic: 行情重连失败，有可能是行情服务故障，也有可能是用户校验信息已过期，需要处理该通知，重新调用NSDK.connect进行连接。
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        # todo 用户信息过期 或者 运维断行情服务

        userid, token, loginAppKey, appSecret = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6"
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(1)
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env="uat")

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001006"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 半自动化
    def test_status_code_1002001007(self):
        """
        1002001007：HTTP网关继续尝试登录
        logic: 登录成功--> 运维关闭平台服务--> 等待20 --> 查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        # todo 运维将行平台服务下线

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001007"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 半自动化
    def test_status_code_1002001008(self):
        """
        1002001008：1002001008：切换 HTTP 连接站点
        logic:
            1、平台站点服务异常，导致在登录过程中当前站点不可用，选择且他站点登录
            2、行情服务token校验失败（token过期），触发站点切换
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        # todo 运维关闭行情认证服务

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001008"
        result = fetch_code(code, self.log_startTS)
        assert result

    # 业务需要理清楚
    def test_status_code_1002001009(self):
        """
        1002001009：行情服务无法校验 token，请重新登录
        logic: 当前行情服务无法验证token，触发1011错误，前端切换站点失败，需要重新调用NSDK.connect进行连接
        step: todo 通过保留一个站点，然后触发互踢。???
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        # todo 通过保留一个站点，然后触发互踢。???

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001009"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 手工通过，自动化需要在看看，为何模拟器上面飞行模式不一样
    def test_status_code_1002001010(self):
        """
        1002001010：行情重新连接成功
        logic: 行情连接出现异常断开，但SDK会自动进行重连，当重连成功后会发送该消息
        step: 登录成功-->断网-->联网-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(5)
        # 飞行模式 todo 真机上 无法操作网络 带排查
        self.androidPage.internet_switch(1)
        time.sleep(30)
        print("========================")
        self.androidPage.internet_switch(2)
        time.sleep(20)
        print("========================")
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001010"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 半自动 待确认切换三次站点时间
    def test_status_code_1002001011(self):
        """
        1002001011：服务异常，登录失败
        logic: 在行情服务验证 token 失败之后进行站点切换登录，只执行三次站点切换，超过三次之后触发服务异常，无法登录，需要重新调用NSDK。connect进行链接
        step: todo 登录成功-->运维关闭行情服务认证-->等待（切换3次要多久）-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        # todo 运维关闭行情认证服务

        self.sdk_login()
        time.sleep(30)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001010"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 手工pass 自动化待实现
    def test_status_code_1002001012(self):
        """
        1002001011：服务异常，登录失败
        logic: 平台服务接口发送请求，服务端异常或断网，重新尝试发送
        step: 登录成功-->断网-->请求键盘精灵接口-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # todo 手机断网


        # 请求键盘精灵接口
        self.androidPage.keyWizard_query_all(code="0005", category="all", market="SH,SZ,HK", begin=0, count=20,
                                             field=None, isQuery=True)
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        code = self.status_code["1002001012"]
        # code = "1002001012"
        result = fetch_code(code, self.log_startTS)
        assert result
