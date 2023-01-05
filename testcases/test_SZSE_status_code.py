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
from util.common import fetch_code, execute_cmd_commind, phone_client_sleep, phone_client_work

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
        driver = self.driver_config()

        self.androidPage = AndBasePage(driver)
        self.envs = self.get_sdk_cfg()['envs']
        self.androidPage.internet_switch(2)
        self.androidPage.imp_wait(1)
        self.status_code = {
            "1002001000": '"code":1002001000',  # pass
            "1002001001": '"code":1002001001',  # pass
            "1002001003": '"code":1002001003',  # pass
            "1002001007": '平台登录重试',  # pass
            "1002001010": '"code":1002001010',  # pass
            "1002001012": 'HTTP请求异常，正在重试',  # pass
            "1002001013": 'HTTP请求失败',  # pass
            "1002001015": '没有可用的连接',  # pass
            "1002001017": 'SDK重复连接',  # pass
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
        userid, token, loginAppKey, appSecret = 12323, 21121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6"
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(1)
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env=env)
        # 模拟器不需要弹窗
        # self.androidPage.phone_permission_enable()
        time.sleep(3)


    # todo bug ,数据太大会把ui撑爆，看不到后续按钮
    # def test_status_code_1002001014(self):
    #     """
    #     1002001014：订阅代码超出上限
    #     step: 登录成功-->行情订阅股票>1000-->查看日志
    #     """
    #     execute_cmd_commind(cmd='adb_logcat')
    #     time.sleep(3)
    #     self.sdk_login()
    #     time.sleep(3)
    #     snapshot_code = "000816.SZ,000817.SZ,000818.SZ,000819.SZ,000821.SZ,000822.SZ,000823.SZ,000825.SZ,000826.SZ,000827.SZ,000828.SZ,000829.SZ,000830.SZ,000831.SZ,000832.SZ,000833.SZ,000836.SZ,000838.SZ,000839.SZ,000848.SZ,000850.SZ,000851.SZ,000852.SZ,000856.SZ,000858.SZ,000859.SZ,000860.SZ,000861.SZ,000862.SZ,000863.SZ,000866.SZ,000868.SZ,000869.SZ,000875.SZ,000876.SZ,000877.SZ,000878.SZ,000880.SZ,000881.SZ,000882.SZ,000883.SZ,000885.SZ,000886.SZ,000887.SZ,000888.SZ,000889.SZ,000892.SZ,000893.SZ,000895.SZ,000897.SZ,002128.SZ,002129.SZ,002130.SZ,002131.SZ,002132.SZ,002133.SZ,002134.SZ,002135.SZ,002136.SZ,002137.SZ,002138.SZ,002139.SZ,002140.SZ,002141.SZ,002142.SZ,002143.SZ,002144.SZ,002145.SZ,002146.SZ,002148.SZ,002149.SZ,002150.SZ,002151.SZ,002152.SZ,002153.SZ,002154.SZ,002155.SZ,002156.SZ,002157.SZ,002158.SZ,002159.SZ,002160.SZ,002161.SZ,002162.SZ,002163.SZ,002164.SZ,002165.SZ,002166.SZ,002167.SZ,002168.SZ,002169.SZ,002170.SZ,002171.SZ,002172.SZ,002173.SZ,002174.SZ,002175.SZ,002177.SZ,002178.SZ,002179.SZ,002180.SZ,002181.SZ,002182.SZ,002183.SZ,002184.SZ,002185.SZ,002186.SZ,002187.SZ,002188.SZ,002189.SZ,002190.SZ,002191.SZ,002193.SZ,002194.SZ,002195.SZ,002196.SZ,002197.SZ,002198.SZ,002199.SZ,002200.SZ,002201.SZ,002202.SZ,002203.SZ,002204.SZ,002205.SZ,002206.SZ,002207.SZ,002208.SZ,002209.SZ,002211.SZ,002212.SZ,002213.SZ,002214.SZ,002215.SZ,002216.SZ,002217.SZ,002218.SZ,002220.SZ,002221.SZ,002222.SZ,002223.SZ,002224.SZ,002225.SZ,002226.SZ,002227.SZ,002228.SZ,002229.SZ,002230.SZ,002231.SZ,002232.SZ,002233.SZ,002234.SZ,002235.SZ,002236.SZ,002237.SZ,002238.SZ,002239.SZ,002240.SZ,002241.SZ,002242.SZ,002243.SZ,002244.SZ,002245.SZ,002246.SZ,002248.SZ,002249.SZ,002250.SZ,002251.SZ,002252.SZ,002253.SZ,002254.SZ,002257.SZ,002258.SZ,002260.SZ,002261.SZ,002262.SZ,002263.SZ,002264.SZ,002265.SZ,002266.SZ,002267.SZ,002268.SZ,002269.SZ,002270.SZ,002271.SZ,002272.SZ,002273.SZ,002274.SZ,002275.SZ,002276.SZ,002277.SZ,002278.SZ,002279.SZ,002281.SZ,002282.SZ,002283.SZ,002284.SZ,002285.SZ,002286.SZ,002287.SZ,002288.SZ,002289.SZ,002290.SZ,002291.SZ,002292.SZ,002293.SZ,002294.SZ,002295.SZ,002296.SZ,002297.SZ,002298.SZ,002299.SZ,002300.SZ,002301.SZ,002302.SZ,002303.SZ,002304.SZ,002305.SZ,002306.SZ,002307.SZ,002308.SZ,002309.SZ,002310.SZ,002311.SZ,002312.SZ,002313.SZ,002314.SZ,002315.SZ,002316.SZ,002317.SZ,002318.SZ,002320.SZ,002321.SZ,002322.SZ,002324.SZ,002325.SZ,002326.SZ,002327.SZ,002328.SZ,002329.SZ,002330.SZ,002331.SZ,002332.SZ,002333.SZ,002334.SZ,002335.SZ,002336.SZ,002337.SZ,002338.SZ,002339.SZ,600238.SH,600239.SH,600240.SH,600246.SH,600248.SH,600249.SH,600250.SH,600251.SH,600252.SH,600253.SH,600256.SH,600257.SH,600258.SH,600259.SH,600260.SH,600261.SH,600262.SH,600263.SH,600265.SH,600266.SH,600267.SH,600268.SH,600269.SH,600270.SH,600271.SH,600272.SH,600273.SH,600275.SH,600276.SH,600277.SH,600278.SH,600279.SH,600281.SH,600282.SH,600283.SH,600284.SH,600285.SH,600286.SH,600287.SH,600288.SH,600291.SH,600292.SH,600293.SH,600295.SH,600296.SH,600297.SH,600298.SH,600299.SH,600300.SH,600301.SH, 600302.SH,600303.SH,600305.SH,600307.SH,600308.SH,600309.SH,600310.SH,600312.SH,600313.SH,600315.SH,600316.SH,60017.SH,600318.SH,600319.SH,600320.SH,600321.SH,600322.SH,600323.SH,600325.SH,600326.SH,600327.SH,600328.SH,600329.SH,600330.SH,600331.SH,600332.SH,600333.SH,600335.SH,600336.SH,600337.SH,600338.SH,600339.SH,600340.SH,600343.SH,600345.SH,600346.SH,600348.SH,600349.SH,600350.SH,600351.SH,600352.SH,600353.SH,600355.SH,600356.SH,600357.SH,600359.SH,600360.SH,600361.SH,600362.SH,600363.SH,600365.SH,600366.SH,600367.SH,600368.SH,600369.SH,600370.SH,600371.SH,600372.SH,600373.SH,600375.SH,600376.SH,600377.SH,600378.SH,600379.SH,600380.SH,600381.SH,600382.SH,600383.SH,600385.SH,600386.SH,600387.SH,600388.SH,600389.SH,600390.SH,600391.SH,600392.SH,600393.SH,600395.SH,600396.SH,600397.SH,600398.SH,600399.SH,600400.SH,600401.SH,600403.SH,600405.SH,600406.SH,600408.SH,600409.SH,600410.SH,600415.SH,600418.SH,600419.SH,600420.SH,600421.SH,600422.SH,600423.SH,600425.SH,600426.SH,600428.SH,600429.SH,600432.SH,600433.SH,600435.SH,600436.SH,600438.SH,600439.SH,600444.SH,600446.SH,600448.SH,600449.SH,600452.SH,600455.SH,600456.SH,600458.SH,600459.SH,600460.SH,600461.SH,600463.SH,600466.SH,600467.SH,600468.SH,600469.SH,600472.SH,600475.SH,600476.SH,600477.SH,600478.SH,600479.SH,600480.SH,600481.SH,600482.SH,600483.SH,600485.SH,600486.SH,600487.SH,600488.SH,600489.SH,600490.SH,600491.SH,600493.SH,600495.SH,600496.SH,600497.SH,600498.SH,600499.SH,600500.SH,600501.SH,600502.SH,600503.SH,600505.SH,600506.SH,600507.SH,600508.SH,600509.SH,600510.SH,600511.SH,600512.SH,600513.SH,600515.SH,600516.SH,600517.SH,600518.SH,600519.SH,600520.SH,600521.SH,600522.SH,600523.SH,600525.SH,600526.SH,600527.SH,600528.SH,600529.SH,600531.SH,600532.SH,600533.SH,600535.SH,600536.SH,600537.SH,600538.SH,600539.SH,600540.SH,600543.SH,600545.SH,600546.SH,600547.SH,600548.SH,600549.SH,600550.SH,600551.SH,600552.SH,600553.SH,600556.SH,600557.SH,600558.SH,600559.SH,600560.SH,600561.SH,600562.SH,600563.SH,600565.SH,600566.SH,600567.SH,600569.SH,600570.SH,600571.SH,600572.SH,600573.SH,600575.SH,600576.SH,600577.SH,600578.SH,600579.SH,600580.SH,600581.SH,600582.SH,600583.SH,600584.SH,600585.SH,600586.SH,600587.SH,600588.SH,600589.SH,600590.SH,600591.SH,600592.SH,600593.SH,600594.SH,600595.SH,600596.SH,600597.SH,600598.SH,600600.SH,600601.SH,600602.SH,600603.SH,600604.SH,600605.SH,600606.SH,600607.SH,600608.SH,600609.SH,600610.SH,600611.SH,600612.SH,600613.SH,600614.SH,600615.SH,600616.SH,600617.SH,600618.SH,600619.SH,600620.SH,600621.SH,600622.SH,600623.SH,600624.SH,600625.SH,600626.SH,600627.SH,600628.SH,600629.SH,600630.SH,600631.SH,600632.SH,600633.SH,600635.SH,600636.SH,600637.SH,600638.SH,600639.SH,600640.SH,600641.SH,600642.SH,600643.SH,600644.SH,600645.SH,600646.SH,600647.SH,600648.SH,600649.SH,600650.SH,600652.SH,600653.SH,600654.SH,600655.SH,600656.SH,600657.SH,600658.SH,600659.SH,600660.SH,600661.SH,600662.SH,600663.SH,600664.SH,600665.SH,600666.SH,600667.SH,600668.SH,600669.SH,600670.SH,600672.SH,600673.SH,600674.SH,600675.SH,600676.SH,600677.SH,600678.SH,600679.SH,600680.SH,600681.SH,600682.SH,600683.SH,600684.SH,600685.SH,600686.SH,600688.SH,600689.SH,600690.SH,600691.SH,600692.SH,600693.SH,600694.SH,600695.SH,600696.SH,600697.SH,600698.SH,600699.SH,600700.SH,600701.SH,600702.SH,600703.SH,600704.SH,600705.SH,600706.SH,600707.SH,600708.SH,600709.SH,600710.SH,600711.SH,600712.SH,600713.SH,600714.SH,600715.SH,600716.SH,600717.SH,600718.SH,600719.SH,600720.SH,600721.SH,000816.SZ,000817.SZ,000818.SZ,000819.SZ,000821.SZ,000822.SZ,000823.SZ,000825.SZ,000826.SZ,000827.SZ,000828.SZ,000829.SZ,000830.SZ,000831.SZ,000832.SZ,000833.SZ,000836.SZ,000838.SZ,000839.SZ,000848.SZ,000850.SZ,000851.SZ,000852.SZ,000856.SZ,000858.SZ,000859.SZ,000860.SZ,000861.SZ,000862.SZ,000863.SZ,000866.SZ,000868.SZ,000869.SZ,000875.SZ,000876.SZ,000877.SZ,000878.SZ,000880.SZ,000881.SZ,000882.SZ,000883.SZ,000885.SZ,000886.SZ,000887.SZ,000888.SZ,000889.SZ,000892.SZ,000893.SZ,000895.SZ,000897.SZ,002128.SZ,002129.SZ,002130.SZ,002131.SZ,002132.SZ,002133.SZ,002134.SZ,002135.SZ,002136.SZ,002137.SZ,002138.SZ,002139.SZ,002140.SZ,002141.SZ,002142.SZ,002143.SZ,002144.SZ,002145.SZ,002146.SZ,002148.SZ,002149.SZ,002150.SZ,002151.SZ,002152.SZ,002153.SZ,002154.SZ,002155.SZ,002156.SZ,002157.SZ,002158.SZ,002159.SZ,002160.SZ,002161.SZ,002162.SZ,002163.SZ,002164.SZ,002165.SZ,002166.SZ,002167.SZ,002168.SZ,002169.SZ,002170.SZ,002171.SZ,002172.SZ,002173.SZ,002174.SZ,002175.SZ,002177.SZ,002178.SZ,002179.SZ,002180.SZ,002181.SZ,002182.SZ,002183.SZ,002184.SZ,002185.SZ,002186.SZ,002187.SZ,002188.SZ,002189.SZ,002190.SZ,002191.SZ,002193.SZ,002194.SZ,002195.SZ,002196.SZ,002197.SZ,002198.SZ,002199.SZ,002200.SZ,002201.SZ,002202.SZ,002203.SZ,002204.SZ,002205.SZ,002206.SZ,002207.SZ,002208.SZ,002209.SZ,002211.SZ,002212.SZ,002213.SZ,002214.SZ,002215.SZ,002216.SZ,002217.SZ,002218.SZ,002220.SZ,002221.SZ,002222.SZ,002223.SZ,002224.SZ,002225.SZ,002226.SZ,002227.SZ,002228.SZ,002229.SZ,002230.SZ,002231.SZ,002232.SZ,002233.SZ,002234.SZ,002235.SZ,002236.SZ,002237.SZ,002238.SZ,002239.SZ,002240.SZ,002241.SZ,002242.SZ,002243.SZ,002244.SZ,002245.SZ,002246.SZ,002248.SZ,002249.SZ,002250.SZ,002251.SZ,002252.SZ,002253.SZ,002254.SZ,002257.SZ,002258.SZ,002260.SZ,002261.SZ,002262.SZ,002263.SZ,002264.SZ,002265.SZ,002266.SZ,002267.SZ,002268.SZ,002269.SZ,002270.SZ,002271.SZ,002272.SZ,002273.SZ,002274.SZ,002275.SZ,002276.SZ,002277.SZ,002278.SZ,002279.SZ,002281.SZ,002282.SZ,002283.SZ,002284.SZ,002285.SZ,002286.SZ,002287.SZ,002288.SZ,002289.SZ,002290.SZ,002291.SZ,002292.SZ,002293.SZ,002294.SZ,002295.SZ,002296.SZ,002297.SZ,002298.SZ,002299.SZ,002300.SZ,002301.SZ,002302.SZ,002303.SZ,002304.SZ,002305.SZ,002306.SZ,002307.SZ,002308.SZ,002309.SZ,002310.SZ,002311.SZ,002312.SZ,002313.SZ,002314.SZ,002315.SZ,002316.SZ,002317.SZ,002318.SZ,002320.SZ,002321.SZ,002322.SZ,002324.SZ,002325.SZ,002326.SZ,002327.SZ,002328.SZ,002329.SZ,002330.SZ,002331.SZ,002332.SZ,002333.SZ,002334.SZ,002335.SZ,002336.SZ,002337.SZ,002338.SZ,002339.SZ,600238.SH,600239.SH,600240.SH,600246.SH,600248.SH,600249.SH,600250.SH,600251.SH,600252.SH,600253.SH,600256.SH,600257.SH,600258.SH,600259.SH,600260.SH,600261.SH,600262.SH,600263.SH,600265.SH,600266.SH,600267.SH,600268.SH,600269.SH,600270.SH,600271.SH,600272.SH,600273.SH,600275.SH,600276.SH,600277.SH,600278.SH,600279.SH,600281.SH,600282.SH,600283.SH,600284.SH,600285.SH,600286.SH,600287.SH,600288.SH,600291.SH,600292.SH,600293.SH,600295.SH,600296.SH,600297.SH,600298.SH,600299.SH,600300.SH,600301.SH,600302.SH,600303.SH,600305.SH,600307.SH,600308.SH,600309.SH,600310.SH,600312.SH,600313.SH,600315.SH,600316.SH,60017.SH,600318.SH,600319.SH,600320.SH,600321.SH,600322.SH,600323.SH,600325.SH,600326.SH,600327.SH,600328.SH,600329.SH,600330.SH,600331.SH,600332.SH,600333.SH,600335.SH,600336.SH,600337.SH,600338.SH,600339.SH,600340.SH,600343.SH,600345.SH,600346.SH,600348.SH,600349.SH,600350.SH,600351.SH,600352.SH,600353.SH,600355.SH,600356.SH,600357.SH,600359.SH,600360.SH,600361.SH,600362.SH,600363.SH,600365.SH,600366.SH,600367.SH,600368.SH,600369.SH,600370.SH,600371.SH,600372.SH,600373.SH,600375.SH,600376.SH,600377.SH,600378.SH,600379.SH,600380.SH,600381.SH,600382.SH,600383.SH,600385.SH,600386.SH,600387.SH,600388.SH,600389.SH,600390.SH,600391.SH,600392.SH,600393.SH,600395.SH,600396.SH,600397.SH,600398.SH,600399.SH,600400.SH,600401.SH,600403.SH,600405.SH,600406.SH,600408.SH,600409.SH,600410.SH,600415.SH,600418.SH,600419.SH,600420.SH,600421.SH,600422.SH,600423.SH,600425.SH,600426.SH,600428.SH,600429.SH,600432.SH,600433.SH,600435.SH,600436.SH,600438.SH,600439.SH,600444.SH,600446.SH,600448.SH,600449.SH,600452.SH,600455.SH,600456.SH,600458.SH,600459.SH,600460.SH,600461.SH,600463.SH,600466.SH,600467.SH,600468.SH,600469.SH,600472.SH,600475.SH,600476.SH,600477.SH,600478.SH,600479.SH,600480.SH,600481.SH,600482.SH,600483.SH,600485.SH,600486.SH,600487.SH,600488.SH,600489.SH,600490.SH,600491.SH,600493.SH,600495.SH,600496.SH,600497.SH,600498.SH,600499.SH,600500.SH,600501.SH,600502.SH,600503.SH,600505.SH,600506.SH,600507.SH,600508.SH,600509.SH,600510.SH,600511.SH,600512.SH,600513.SH,600515.SH,600516.SH,600517.SH,600518.SH,600519.SH,600520.SH,600521.SH,600522.SH,600523.SH,600525.SH,600526.SH,600527.SH,600528.SH,600529.SH,600531.SH,600532.SH,600533.SH,600535.SH,600536.SH,600537.SH,600538.SH,600539.SH,600540.SH,600543.SH,600545.SH,600546.SH,600547.SH,600548.SH,600549.SH,600550.SH,600551.SH,600552.SH,600553.SH,600556.SH,600557.SH,600558.SH,600559.SH,600560.SH,600561.SH,600562.SH,600563.SH,600565.SH,600566.SH,600567.SH,600569.SH,600570.SH,600571.SH,600572.SH,600573.SH,600575.SH,600576.SH,600577.SH,600578.SH,600579.SH,600580.SH,600581.SH,600582.SH,600583.SH,600584.SH,600585.SH,600586.SH,600587.SH,600588.SH,600589.SH,600590.SH,600591.SH,600592.SH,600593.SH,600594.SH,600595.SH,600596.SH,600597.SH,600598.SH,600600.SH,600601.SH,600602.SH,600603.SH,600604.SH,600605.SH,600606.SH,600607.SH,600608.SH,600609.SH,600610.SH,600611.SH,600612.SH,600613.SH,600614.SH,600615.SH,600616.SH,600617.SH,600618.SH,600619.SH,600620.SH,600621.SH,600622.SH,600623.SH,600624.SH,600625.SH,600626.SH,600627.SH,600628.SH,600629.SH,600630.SH,600631.SH,600632.SH,600633.SH,600635.SH,600636.SH,600637.SH,600638.SH,600639.SH,600640.SH,600641.SH,600642.SH,600643.SH,600644.SH,600645.SH,600646.SH,600647.SH,600648.SH,600649.SH,600650.SH,600652.SH,600653.SH,600654.SH,600655.SH,600656.SH,600657.SH,600658.SH,600659.SH,600660.SH,600661.SH,600662.SH,600663.SH,600664.SH,600665.SH,600666.SH,600667.SH,600668.SH,600669.SH,600670.SH,600672.SH,600673.SH,600674.SH,600675.SH,600676.SH,600677.SH,600678.SH,600679.SH,600680.SH,600681.SH,600682.SH,600683.SH,600684.SH,600685.SH,600686.SH,600688.SH,600689.SH,600690.SH,600691.SH,600692.SH,600693.SH,600694.SH,600695.SH,600696.SH,600697.SH,600698.SH,600699.SH,600700.SH,600701.SH,600702.SH,600703.SH,600704.SH,600705.SH,600706.SH,600707.SH,600708.SH,600709.SH,600710.SH,600711.SH,600712.SH,600713.SH,600714.SH,600715.SH,600716.SH,600717.SH,600718.SH,600719.SH,600720.SH,600721.SH"
    #
    #     # 请求行情订阅接口
    #     self.androidPage.snapshot_subscription(snapshot_code=snapshot_code, fields="code,last,change")
    #     time.sleep(10)
    #     execute_cmd_commind(cmd='adb_close')
    #     time.sleep(3)
    #     # code = self.status_code["1002001012"]
    #     code = "1002001014"
    #     result = fetch_code(code, self.log_startTS)
    #     assert result


    def test_status_code_1002001000(self):
        """1002001000：建立行情连接成功"""
        execute_cmd_commind(cmd='adb_logcat')
        self.sdk_login()
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(5)
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
        time.sleep(5)
        code = self.status_code["1002001001"]
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
        time.sleep(5)
        code = self.status_code["1002001003"]
        result = fetch_code(code, self.log_startTS)
        assert result

    # todo 这个case需要链接模拟器，appium不支持真机高版本
    def test_status_code_1002001007(self):
        """
        1002001007：平台登录重试
        logic: 登录成功--> 运维关闭平台服务--> 等待20 --> 查看日志
        step: 飞行模式-->登录->请求键盘精灵-->查看日志
        """
        self.androidPage.internet_switch(1)
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(10)
        code = self.status_code["1002001007"]
        result = fetch_code(code, self.log_startTS)
        assert result

    # 只能模拟器上运行，因为appium支持系统版本低，现有的都不符合，详情请看最上面备注
    def test_status_code_1002001012(self):
        """
        1002001012：HTTP请求异常，正在重试
        logic: 平台服务接口发送请求，服务端异常或断网，重新尝试发送
        step: 登录成功-->断网-->请求键盘精灵接口-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        # 手机断网
        self.androidPage.internet_switch(1)
        # 请求键盘精灵接口
        self.androidPage.keyWizard_query_all(code="0005", category="all", market="SH,SZ,HK", begin=0, count=20,
                                             field=None, isQuery=True)
        time.sleep(20)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        code = self.status_code["1002001012"]
        # code = "1002001012"
        result = fetch_code(code, self.log_startTS)
        assert result

    def test_status_code_1002001013(self):
        """
        1002001013：HTTP请求失败
        logic: 平台服务接口发送请求后，服务端异常情况
            1、在触发三次重新发送依然不成功
            2、重新执行 GSession 的登录流程（包括登录三次重试，HTTP 站点切换）
            3、重新登录失败，返回通知消息
        step: 登录成功-->断网-->请求键盘精灵-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(3)
        self.androidPage.internet_switch(1)
        time.sleep(3)

        # 请求键盘精灵接口
        self.androidPage.keyWizard_query_all(code="0005", category="all", market="SH,SZ,HK", begin=0, count=20,
                                             field=None, isQuery=True)
        time.sleep(20)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(3)
        code = self.status_code["1002001013"]
        result = fetch_code(code, self.log_startTS)
        assert result

    def test_status_code_1002001015(self):
        """
        1002001015：没有可用的连接
        logic: 在NSDK没有执行连接，或者连接断开场景下，发送数据请求
            1，行情服务注定断开，clearData
            2，token 验证失败消息状态码是 5 或者1001001007，切换站点之前，clearData
            3，行情服务重连失败，clearData
            4，平台服务登录失败，clearData
            5，用户调用 disconnect，clearData
        step: 未登录 or disconnect-->请求键盘精灵接口-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(3)
        # 请求键盘精灵接口
        self.androidPage.keyWizard_query_all(code="0005", category="all", market="SH,SZ,HK", begin=0, count=20,
                                             field=None, isQuery=True)
        time.sleep(15)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(10)
        code = self.status_code["1002001015"]
        # code = "1002001015"
        result = fetch_code(code, self.log_startTS)
        assert result
    def test_status_code_1002001017(self):
        """
        1002001017：SDK重复连接
        logic: NSDK在连接成功或者重连中状态，再次调用 connect 进行连接
        step: 登录成功-->再次登录-->查看日志
        """
        execute_cmd_commind(cmd='adb_logcat')
        time.sleep(3)
        self.sdk_login()
        time.sleep(5)
        userid, token, loginAppKey, appSecret = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6"
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env="uat")

        time.sleep(10)
        execute_cmd_commind(cmd='adb_close')
        time.sleep(10)
        code = self.status_code["1002001017"]
        # code = "1002001017"
        result = fetch_code(code, self.log_startTS)
        assert result