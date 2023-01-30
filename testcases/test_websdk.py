# encoding: utf-8
import json

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
data_dir = os.path.join(os.path.dirname(cur_dir), "data")

"""
SDK_KEYWIZARD_CATEGORY_ALL ：所有
SDK_KEYWIZARD_CATEGORY_BOND: 债券
SDK_KEYWIZARD_CATEGORY_FOND: 基金
SDK_KEYWIZARD_CATEGORY_INDEX: 指数
SDK_KEYWIZARD_CATEGORY_OPTION: 期权
SDK_KEYWIZARD_CATEGORY_STOCK: 股票
SDK_KEYWIZARD_MARKET_SHSZHK： 深圳信
"""


class TestWebSDK:
    def setup(self):
        driver = webdriver.Chrome()
        self.webSDK = WebSDKPage(driver)
        login_params = self.get_websdk_cfg()
        user_id, user_token, env, auth_env, appKey, appSecert, other_params, enable_ssl, self.envs = login_params.values()
        self.login(user_id, user_token, env, auth_env, appKey, appSecert, other_params, enable_ssl)

    def setup_class(self):
        pass

    def teardown(self):
        self.webSDK.close()

    def teardown_class(self):
        pass

    def get_websdk_cfg(self):
        web_sdk_cf = os.path.join(data_dir, "web_sdk.json")
        with open(web_sdk_cf, "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def set_env_config_old(env):
        envs = """
        [
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
            ]
            
        """

        add_env_cmd = f"NSDK.addEnvType({envs});"
        set_env_cmd = f"NSDK.setEnvType('{env}')"
        return [add_env_cmd, set_env_cmd]
        # execjs.compile(add_env_cmd)
        # execjs.compile(which_env)

    def login(self, user_id, user_token, env, auth_env, appKey, appSecert, other_params, enable_ssl):
        websdk = self.webSDK
        websdk.open_env()
        # cmds = self.set_env_config("uat")
        # websdk.exec_js_cmd(cmds)

        cmds = self.set_env_config_old("uat")
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

    @pytest.mark.parametrize("pageNo, pageSize, keyword, fields", [
        (0, 10, "000", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "0", "sufSecuCode,secuAbbr,ExchgMarket"),
    ]
                             )
    def test_keword_fuzzy_query_PQMR_1074(self, pageNo, pageSize, keyword, fields):
        """
        模糊查询
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        titles = self.webSDK.get_result_title()
        # 校验查询结果集字段等于请求字段，需要转换对比
        assert fields.lower() == titles.replace(" ", ",")
        tbody = self.webSDK.get_search_result()
        time.sleep(6)
        stocks = tbody.split("\n")
        for stock in stocks:
            assert stock.startswith(keyword)
        assert len(stocks) <= pageSize

    @pytest.mark.parametrize("pageNo, pageSize, keyword, fields", [
        (0, 10, "平安", "sufSecuCode,secuAbbr,ExchgMarket"),
    ]
                             )
    def test_keword_fuzzy_query_PQMR_1077(self, pageNo, pageSize, keyword, fields):
        """
        键盘精灵支持名称模糊匹配
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        titles = self.webSDK.get_result_title()
        # 校验查询结果集字段等于请求字段，需要转换对比
        assert fields.lower() == titles.replace(" ", ",")
        tbody = self.webSDK.get_search_result()
        time.sleep(6)
        stocks = tbody.split("\n")
        for stock in stocks:
            assert keyword in stock
        assert len(stocks) <= pageSize

    @pytest.mark.parametrize("pageNo, pageSize, keyword, fields", [
        (0, 10, "pazq", "sufSecuCode,secuAbbr,ExchgMarket"),
    ]
                             )
    def test_keword_fuzzy_query_PQMR_1079(self, pageNo, pageSize, keyword, fields):
        """
        键盘精灵支持名称缩写模糊匹配
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        titles = self.webSDK.get_result_title()
        # 校验查询结果集字段等于请求字段，需要转换对比
        assert fields.lower() == titles.replace(" ", ",")
        tbody = self.webSDK.get_search_result()
        time.sleep(6)
        stocks = tbody.split("\n")
        assert stocks
        assert len(stocks) <= pageSize

    @pytest.mark.parametrize("pageNo, pageSize, keyword, fields", [
        (0, 10, ",", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "1234325342", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "", "sufSecuCode,secuAbbr,ExchgMarket"),
    ]
                             )
    def test_keword_err_query_PQMR_1076(self, pageNo, pageSize, keyword, fields):
        """
        键盘精灵输入异常符号查询为空
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        tbody = self.webSDK.get_search_result()
        assert tbody == ""

    @pytest.mark.parametrize("pageNo, pageSize, keyword,fields", [
        (0, 10, "平安银行", "sufSecuCode,secuAbbr,ExchgMarket"),
    ]
                             )
    def test_keword_precise_query_PQMR_1258(self, pageNo, pageSize, keyword, fields):
        """
        精确查询
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        titles = self.webSDK.get_result_title()
        # 校验查询结果集字段等于请求字段，需要转换对比
        assert fields.lower() == titles.replace(" ", ",")
        tbody = self.webSDK.get_search_result()
        stocks = tbody.split()
        assert stocks[1] == keyword
        assert len(stocks) <= pageSize

    @pytest.mark.parametrize("pageNo, pageSize, keyword,fields", [
        (0, 10, "300002", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "002607", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "600213", "sufSecuCode,secuAbbr,ExchgMarket"),
        (0, 10, "399975", "sufSecuCode,secuAbbr,ExchgMarket"),
        # (0, 10, "202007", "sufSecuCode,secuAbbr,ExchgMarket"), # todo 这个股票没有
        # (0, 10, "124044", "sufSecuCode,secuAbbr,ExchgMarket"), # todo 这个股票没有
        (0, 10, "118000", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询可转债
        (0, 10, "152800", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询企业债
        (0, 10, "010303", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询国债
        (0, 10, "508000", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询REITs
        (0, 10, "501000", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询LOF
        (0, 10, "516150", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询ETF
        (0, 10, "508027", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询封闭式基金
        (0, 10, "600000", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询A股股票
        (0, 10, "900901", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询B股股票
        (0, 10, "688001", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询科创版股票
    ]
                             )
    def test_keyword_precise_query_by_code(self, pageNo, pageSize, keyword, fields):
        """
        精确查询
        :param pageNo:
        :param pageSize:
        :param keyword:
        :return: No
        """
        seachKeyWord_cmd = self.webSDK.search_key_js(pageNo, pageSize, keyword, fields)
        self.webSDK.exec_js_cmd(seachKeyWord_cmd)
        time.sleep(6)
        titles = self.webSDK.get_result_title()
        # 校验查询结果集字段等于请求字段，需要转换对比
        assert fields.lower() == titles.replace(" ", ",")
        tbody = self.webSDK.get_search_result()
        stocks = tbody.split()
        assert stocks[0].split(".")[0] == keyword
        assert len(stocks) <= pageSize

    @pytest.mark.parametrize("stock,fields", [
        ("600123.SH", "Code,Name,SectorID,SectorName,MarginTrade,StockConnect"),
        ("600123.SH,600000.SH", "Code,Name,SectorID,SectorName,MarginTrade,StockConnect"),
        ("600123.SH,600000.SH", "Code"),
    ])
    def test_single_stock(self, stock, fields):
        single_stock_cmd = self.webSDK.singel_stock_js(stocks=stock, fields=fields)
        self.webSDK.exec_js_cmd(single_stock_cmd)
        time.sleep(1)
        tbody = self.webSDK.get_search_result()
        time.sleep(2)
        if "," in stock:
            tbody = tbody.split("\n")
            for idx, sto in enumerate(tbody):
                assert sto.split()[0] == stock.split(",")[idx]
        else:
            assert tbody.startswith(stock)
        fields_lower = fields.lower().replace(",", " ")
        title = self.webSDK.get_result_title()
        time.sleep(3)
        assert fields_lower == title

    @pytest.mark.parametrize("stock,fields", [
        ("", "Code,Name,SectorID,SectorName,MarginTrade,StockConnect"),  # 个股信息空查询
        ("600123.SH,600000.SH", ""),  # 个股信息查询字段为空
    ])
    def test_single_stock_err(self, stock, fields):
        single_stock_cmd = self.webSDK.singel_stock_js(stocks=stock, fields=fields)
        self.webSDK.exec_js_cmd(single_stock_cmd)
        time.sleep(1)
        tbody = self.webSDK.get_search_result()
        assert tbody == ""
