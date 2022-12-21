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
from util.common import fetch_code,execute_cmd_commind

logger = get_logger()
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")
data_dir = os.path.join(os.path.dirname(cur_dir), "data")


class TestAndroidSDK:
    def setup(self):
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
        # self.androidPage.impower()
        # self.sdk_login()

    def setup_class(self):
        pass

    def teardown(self):
        # self.androidPage.quit()
        pass

    def teardown_class(self):
        pass

    def get_sdk_cfg(self):
        web_sdk_cf = os.path.join(data_dir, "web_sdk.json")
        with open(web_sdk_cf, "r") as f:
            data = json.load(f)
        return data

    @pytest.mark.parametrize("userid,token,loginAppKey,appSecret,env", [
        (123121231, 2313121, "778_Mobile_34", "$2a$10$PT8Nig9yoNyJAqOBXbsKwuDNTC2HIaoOqQrQhQEcF9eOFWWZR.C8q", "uat"),
    ])
    def test_sdk_login(self, userid, token, loginAppKey, appSecret, env):
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env=env)

    def sdk_login(self):
        # userid, token, loginAppKey, appSecret, env = 123121231, 2313121, "778_Mobile_34", "$2a$10$PT8Nig9yoNyJAqOBXbsKwuDNTC2HIaoOqQrQhQEcF9eOFWWZR.C8q", "uat"
        userid, token, loginAppKey, appSecret, env = 123121231, 2313121, "234232_Mobile_71", "$2a$10$pGPlIyS7NWdgza6N.UkeaOoRwZ8.LvbsJp.CTdAF33q8O4ifg7MB6", "uat"
        self.androidPage.envs_import_busy(self.envs, busy='import_accept')
        time.sleep(1)
        self.androidPage.connect_server(userid=userid, token=token, loginAppKey=loginAppKey, appSecret=appSecret,
                                        env=env)
        self.androidPage.phone_permission_enable()

    def test_sector_stream(self):
        """
        添加板块-->查询板块-->修改板块-->移动板块-->删除板块
        :return: None
        """
        self.sdk_login()

        # 添加板块
        sector_name = "我的板块" + str(int(time.time()))[5:]
        self.androidPage.sector_add(sector_name=sector_name)

        # 查询板块
        result = self.androidPage.sector_query()
        assert sector_name in result.keys()

        # 返回上一页
        self.androidPage.last_back()

        # 修改板块
        sector_rename = "修改板块名称" + str(int(time.time()))[5:]
        sector_id, isUp = result[sector_name], True
        self.androidPage.sector_update(sector_id, sector_name=sector_rename, isUp=True)

        # 名称：id
        update_res = self.androidPage.sector_query()
        for k, v in update_res.items():
            # id 如果与上一次查询相等就判断 他的值是否变更。
            if v == result[sector_name]:
                # 校验修改内容
                assert k == sector_rename

        # 返回上一页
        self.androidPage.last_back()

        # 添加板块
        sector_name_2 = "我的板块2" + str(int(time.time()))[5:]
        self.androidPage.sector_add(sector_name=sector_name_2)

        # 移动板块
        move_idx = 1
        self.androidPage.sector_move(sector_id, index=move_idx)
        sector_move_res = self.androidPage.sector_query()

        # 校验移动位置
        for idx, dic in enumerate(sector_move_res.values()):
            if sector_id == dic:
                assert idx == move_idx

        # 返回上一页
        self.androidPage.last_back()
        del_befor_size = len(sector_move_res)

        # 删除板块
        self.androidPage.sector_delete(sector_id)
        del_after_size = len(self.androidPage.sector_query())
        # 校验数据少了一条
        assert del_befor_size - 1 == del_after_size

    # todo 待完善
    def test_owner_stock_add(self):
        sectors = self.androidPage.sector_query()
        self.androidPage.last_back()
        # {'修改板块名称42259': '17d4cab1-9d46-4c0d-bb56-ec21a319375e', '我的板块208060': '4ea20cc5-55f7-44e3-837d-f3c71232de8f'} 600213.SH
        sector_id = sectors['我的板块208060']
        self.androidPage.owner_stock_add(sector_id=sector_id, stock_code='600213.SH')
        self.androidPage.owner_stock_query(sector_id=sector_id)


    # todo 存在 appium版本兼容问题
    def test_status_code_1002001000(self):
        """1002001000：建立行情连接成功"""
        execute_cmd_commind(cmd='logcat')
        self.sdk_login()
        self.androidPage.imp_wait(20)
        execute_cmd_commind(cmd='adb_close')
        result = fetch_code("1002001000")
        assert result



    def test_status_code_1002001001(self):
        """1002001001：断开行情连接成功"""
        # execute_cmd_commind(cmd='clear')
        self.sdk_login()
        execute_cmd_commind(cmd='logcat')
        self.androidPage.imp_wait(10)
        self.androidPage.disconnect()
        self.androidPage.imp_wait(20)
        # self.androidPage.imp_wait(5)
        execute_cmd_commind(cmd='adb_close')
        code = "1002001001"
        result = fetch_code(code)
        print(result)
        assert result