# encoding: utf-8
import allure
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.indexPage import IndexPage
import time
from selenium.webdriver import ActionChains
import pytest
from util.common import get_logger, start_webdriver, get_env_data
from exec.myexe import *
import os
from pages.websdkPage import WebSDKPage
from selenium import webdriver
import execjs

logger = get_logger()
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")


class TestWebSDK:
    def setup(self):
        driver = webdriver.Chrome()
        self.webSDK = WebSDKPage(driver)
        user_id, user_token, env, auth_env = "3423224", "12313", "uat", "dev"
        appKey, appSecert, other_params, enable_ssl = "5551_PC_42", "$2a$10$nf6bHoHaY6GsfvplrQZqde.H.q.IbHR.9msI1Qv5Zi8QerbZxyfC2", "", "use"
        self.login(user_id, user_token, env, auth_env, appKey, appSecert, other_params, enable_ssl)

    def setup_class(self):
        pass

    def teardown(self):
        self.webSDK.close()

    def teardown_class(self):
        pass

    @staticmethod
    def set_env_config(env):
        add_env_cmd = """
                        NSDK.addEnvType([
                    {
                        name: 'szse_dev',
                        httpHostName : `dev-datasdk.mktdata.cn`,
                        wsHostName : `dev-quotesdk.mktdata.cn`,
                        customWsHostName: `dev-customize-sdk.mktdata.cn`,
                        siteList : [
                            "dev-shlistsdk.mktdata.cn/application/",
                            "dev-gzlistsdk.mktdata.cn/application/"
                        ]
                    },
                    {
                        name: 'dev',
                        httpHostName:`dev-platform.hongwuniu.com`,
                        wsHostName:`dev-quote.hongwuniu.com`,
                        customWsHostName:`dev-customize-sdk.hongwuniu.com`,
                        siteList:[
                            "dev-shlistsdk.hongwuniu.com/application/",
                            "dev-gzlistsdk.hongwuniu.com/application/" 
                        ]
                    },
                    {
                        name: 'test',
                        httpHostName:`test-platform.hongwuniu.com`,
                        wsHostName:`test-quote.hongwuniu.com`,
                        customWsHostName:`test-customize-sdk.hongwuniu.com`,
                        siteList:[
                            "test-shlistsdk.hongwuniu.com/application/",
                            "test-gzlistsdk.hongwuniu.com/application/"
                        ]
                    },
                    {
                        name: 'uat',
                        httpHostName:`uat-platform.hongwuniu.com`,
                        wsHostName:`uat-quote.hongwuniu.com`,
                        customWsHostName:`uat-customize-sdk.hongwuniu.com`,
                        siteList:[
                            "uat-shlistsdk.hongwuniu.com/application/",
                            "uat-gzlistsdk.hongwuniu.com/application/"  
                        ]
                    },
                    {
                        name: 'pro',
                        httpHostName : `platform.hongwuniu.com`,
                        wsHostName : `quote.hongwuniu.com`,
                        customWsHostName:`customize-sdk.hongwuniu.com`,
                        siteList : [
                            "shlistsdk.hongwuniu.com/application/",
                            "gzlistsdk.hongwuniu.com/application/",
                        ]
                    }
                ])
                        """
        which_env_cmd = f"NSDK.setEnvType('{env}');"
        return [add_env_cmd, which_env_cmd]
        # execjs.compile(add_env_cmd)
        # execjs.compile(which_env)

    def login(self, user_id, user_token, env, auth_env, appKey, appSecert, other_params, enable_ssl):
        websdk = self.webSDK
        websdk.open_env()
        cmds = self.set_env_config("uat")
        for cmd in cmds:
            websdk.exec_js_cmd(cmd)
        websdk.connect_server()
        websdk.input_userId(user_id)
        websdk.input_token(user_token)
        websdk.input_env(env)
        websdk.input_auth_env(auth_env)
        websdk.input_appkey(appKey)
        websdk.input_appsert(appSecert)
        websdk.input_others_params(other_params)
        websdk.enable_ssl(enable_ssl)
        websdk.login()
        time.sleep(5)

    @pytest.mark.parametrize("pageNo, pageSize, keyword", [
        (1, 10, "000")]
                             )
    def test_keword_search(self, pageNo, pageSize, keyword):
        # pageNo, pageSize, keyword = 1, 10, "000"
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        tbody = self.webSDK.get_search_result()
        time.sleep(6)
        stocks = tbody.split("\n")
        for stock in stocks:
            assert stock.startswith(keyword)
        assert len(stocks) == pageSize

    @pytest.mark.parametrize("stock,fields", [("600123.SH", "Code,Name,SectorID,SectorName,MarginTrade,StockConnect")])
    def test_single_stock(self, stock, fields):
        single_stock_cmd = self.webSDK.singel_stock_js(stocks=stock, fields=fields)
        self.webSDK.exec_js_cmd(single_stock_cmd)
        tbody = self.webSDK.get_search_result()
        time.sleep(6)
        fields_lower = fields.lower().replace(",", " ")
        title = self.webSDK.get_result_title()
        assert fields_lower == title
        assert tbody.startswith(stock)
