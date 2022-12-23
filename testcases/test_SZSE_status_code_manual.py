# coding=utf-8
import time


"""
appium 网络设置平台机型支持
http://appium.io/docs/cn/writing-running-appium/other/network-connection/
iOS
不幸的是，目前 Appium 不支持这个 API。
Android

Android 上有如下限制：
真机

    只能在 Android 6 或者以下，改变飞行模式
    只能在 Android 4.4 或者以下改变数据连接状态。5.0 或者以上必须 root 了之后才能工作。(比如，可以运行 su )
    所有的 Android 版本都能改变 WI-FI 连接状态

模拟器

    只能在 Android 6 或者以下，改变飞行模式
    所有的 Android 版本都能改变数据连接
    所有的 Android 版本都能改变 WI-FI 连接状态

Windows

不幸的是，目前 Appium 测试 Windows 应用，不支持这个 API。
"""

from selenium import webdriver
from pages.androidPage import AndBasePage
from util.common import get_logger
import os
import json
from util.common import fetch_code, execute_cmd_commind
from util.pytest_utils import execute_manual_step


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
        self.androidPage.internet_switch(2)
        self.androidPage.imp_wait(1)
        self.status_code = {
            "1002001000": '{"message":"登录成功,行情已开启","code":1002001000}',  # pass
            "1002001001": '{"message":"主行情连接正常关闭","code":1002001001}',  # pass
            "1002001002": '{"message":"行情连接异常断开,正在重连","code":1002001002}',  # pass
            "1002001003": '{"message":"HTTP网关登录失败，请重新登录","code":1002001003}',  # pass
            "1002001007": '{"message":"HTTP网关继续尝试登录","code":1002001007}',  # pass
            "1002001010": '{"message":"行情重连成功","code":1002001010}',  # pass
            "1002001012": '{"message":"HTTP请求异常，正在重试","code":1002001012}',  # pass
            "1002001013": '{"message":"HTTP请求失败","code":1002001013}',  # pass
            "1002001015": '{"message":"没有可用的连接","code":1002001015}',  # pass
            "1002001017": '{"message":"sdk重复连接","code":1002001017}',  # pass
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
        # self.androidPage.phone_permission_enable()

    # todo 手动测试通过，自动化和模拟器需要在看看问题
    def test_status_code_1002001002(self):
        """1002001002：行情连接断开，正在尝试重连
        logic: 由于服务端故障、网络中断、客户端休眠等原因导致与行情服务的连接异常断开，SDK会自动进行重连，客户无需处理
        """
        self.sdk_login()
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        # todo
        execute_manual_step("请断开手机网络？")
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001002"
        result = fetch_code(code, self.log_startTS)
        assert result



    def test_status_code_1002001003_platformServer_disconnect(self):
        """
        1002001003：建立行情连接失败，平台登录失败
        logic: 登录后飞行模式--> 切到wify --> 等待20 --> 查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # todo 平台登录失败
        execute_manual_step("运维下线平台服务了？")


        time.sleep(3)
        execute_cmd_commind(cmd='adb_close')
        # code = self.status_code["1002001001"]
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result


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
        execute_manual_step("运维下线行情服务了？")


        execute_cmd_commind(cmd='adb_close')
        # code = self.status_code["1002001001"]
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result


    def test_status_code_1002001005(self):
        """
        1002001005：行情服务主动断开与SDK的连接：XXXX
        logic: 由于异常调用或多点登录限制引起的行情服务主动断开连接，该信息主要用于分析断开原因，无需处理
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        execute_manual_step("请另外一台手机登录相同账号")


        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001005"
        result = fetch_code(code, self.log_startTS)
        assert result

    def test_status_code_1002001006(self):
        """
        1002001006：行情连接断开且自动重连失败，请重新登录
        logic: 行情重连失败，有可能是行情服务故障，也有可能是用户校验信息已过期，需要处理该通知，重新调用NSDK.connect进行连接。
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        # todo 用户信息过期 或者 运维断行情服务
        execute_manual_step("运维断行情服务了？")

        time.sleep(3)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001006"
        result = fetch_code(code, self.log_startTS)
        assert result
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
        execute_manual_step("运维关闭平台站点服务了？")

        time.sleep(3)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001008"
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 半自动化 业务需要理清楚
    def test_status_code_1002001009(self):
        """
        1002001009：行情服务无法校验 token，请重新登录
        logic: 当前行情服务无法验证token，触发1011错误，前端切换站点失败，需要重新调用NSDK.connect进行连接
        step: todo 通过保留一个站点，然后触发互踢。???
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # todo 通过保留一个站点，然后触发互踢。???
        execute_manual_step("运维关闭平台站点服务了？")


        time.sleep(3)
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
        execute_manual_step("请先断网-->行情出现异常-->联网？")

        time.sleep(3)
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
        self.sdk_login()
        # todo 运维关闭行情认证服务
        execute_manual_step("运维关闭行情认证服务了？")


        time.sleep(3)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001001"]
        code = "1002001011"
        result = fetch_code(code, self.log_startTS)
        assert result



    # todo 运维下线平台服务接口
    def test_status_code_1002001016(self):
        """
        1002001016：刷新token失败，错误信息由平台服务返回
        logic: token刷新失败，连接断开，需要重新调用NSDK.connect进行连接
            1，行情登录成功，在 GQuoteWsBase 的 this.onopen 中执行 getToken 获取
                a:行情首次登录
                b:行情 Token 验证失败，触发站点切换之后的重新登录
            2，刷新 token 定时器触发，GTenant 的 resetRefreshTokenTimer
                a: 根据登录成功返回的 expores_in 计算出过妻子，然在过期三分钟前重新获取 access_token
        step: todo 登录成功-->运维下线平台获取token接口-->等-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(3)
        # todo 运维下线平台服务接口
        execute_manual_step("运维下线平台服务接口了？")

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        # code = self.status_code["1002001012"]
        code = "1002001016"
        result = fetch_code(code, self.log_startTS)
        assert result

