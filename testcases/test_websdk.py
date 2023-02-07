# encoding: utf-8
import json
from datetime import datetime

import allure
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.indexPage import IndexPage
import time
from selenium.webdriver import ActionChains
import pytest
from util.common import get_logger, start_webdriver, get_env_data, str_to_stamp
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        (0, 10, "399481", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询债券指数(.SZ)
        (0, 10, "501005", "sufSecuCode,secuAbbr,ExchgMarket"),  # 查询ETF基金(.SH)
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
        self.webSDK.set_js_value(seachKeyWord_cmd)
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
        self.webSDK.set_js_value(single_stock_cmd)
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
        cmd = self.webSDK.singel_stock_js(stocks=stock, fields=fields)
        self.webSDK.set_js_value(cmd)
        self.webSDK.exec_js_cmd(cmd)
        time.sleep(1)
        tbody = self.webSDK.get_search_result()
        assert tbody == ""

    @pytest.mark.parametrize("stock", [
        ("000001.SH")
    ])
    def test_snapshotUpdowns(self, stock):
        cmd = self.webSDK.snapshotUpdowns_js(stock_code=stock)
        self.webSDK.set_js_value(cmd)
        self.webSDK.exec_js_cmd(cmd)
        time.sleep(1)
        tbody = self.webSDK.get_search_result()
        assert tbody.startswith(stock)
        pre_titles = 'Code RiseCount SuspensionCount FallCount ScopeName ScopeValue'
        real_titles = self.webSDK.get_result_title()
        assert real_titles == pre_titles

    @pytest.mark.parametrize("stock", [
        ("")
    ])
    def test_snapshotUpdowns_err(self, stock):
        cmd = self.webSDK.snapshotUpdowns_js(stock_code=stock)
        self.webSDK.set_js_value(cmd)
        self.webSDK.exec_js_cmd(cmd)
        time.sleep(1)
        tbody = self.webSDK.get_search_result()
        assert tbody == ""

    @pytest.mark.parametrize("stock_code,startDay,endDay,fields,isSubcrible,size,period", [
        ("600000.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_DAY"),  # 查看A股的日K线
        ("900901.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_DAY"),  # 查看B股的默认日K线
        ("510010.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_DAY"),  # 查看ETF的默认日K线
        ("010303.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_DAY"),  # 查看债券的默认日K线
        ("600000.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_MONTH"),  # 查看A股的月K线字段
        ("900901.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_MONTH"),  # 查看B股的月K线字段
        ("510010.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_MONTH"),  # 查看ETF的月K线字段
        ("010303.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_MONTH"),  # 查看债券的月K线字段
        ("600000.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_YEAR"),  # 查看A股的年K线字段
        ("900901.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_YEAR"),  # 查看B股的年K线字段
        ("510010.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_YEAR"),  # 查看ETF的年K线字段
        ("010303.SH", "20230110", "20230130", "$all", "true", 10, "SDK_KLINE_PERIOD_YEAR"),  # 查看债券的年K线字段
        # ("600000.SH", "20230110", "20230130", "$all", "true", 10,"SDK_KLINE_PERIOD_DAY"),
        # ("600000.SH", "20230110", "20230130", "date", "true", 10,"SDK_KLINE_PERIOD_DAY"),
        # ("600000.SH", "20230110", "20230130", "date,open", "true", 10,"SDK_KLINE_PERIOD_DAY"),
        # ("600000.SH", "20201124", "20210315", "$all", "true", 10,"SDK_KLINE_PERIOD_DAY"),  #
    ])
    def test_kline_normal(self, stock_code, startDay, endDay, fields, isSubcrible, size, period):
        """
        查看K线字段
        """
        all_fields = "date open high low close volume amount deallots"
        cmd = self.webSDK.kLine_js(stock_code=stock_code, startDay=startDay, endDay=endDay, fields=fields,
                                   isSubcrible=isSubcrible, size=size, period=period)
        self.webSDK.set_js_value(cmd)
        self.webSDK.exec_js_cmd(cmd)
        kline_result = self.webSDK.get_search_result()
        time.sleep(2)
        kline_titles = self.webSDK.get_result_title()
        if fields == "$all":
            assert kline_titles.lower() == all_fields
        else:
            if "," in fields:
                fields = fields.replace(",", " ")
            assert kline_titles.lower() == fields
        klines = kline_result.split("\n")
        # 校验查询长度
        assert len(klines) <= size

        def check_date_gap(klines):
            # 校验日期间隔 todo 也存在某段时间缺数据的情况，所以间隔不好校验
            date_interval = {"SDK_KLINE_PERIOD_DAY": 1, "SDK_KLINE_PERIOD_MONTH": 28, "SDK_KLINE_PERIOD_YEAR": 360}
            # 返回只有 2023/01/17 这种格式的数据
            klines = list(map(lambda x: x.split()[0], klines))
            klines = list(map(lambda x: datetime.strptime(x, "%Y/%m/%d"), klines))
            # todo 也存在某段时间缺数据的情况，不好校验
            for i in range(len(klines)):
                if date_interval[period] == 1:
                    assert (klines[i + 1] - klines[i]).days == date_interval[period]
                elif date_interval[period] == 28:
                    assert (klines[i + 1] - klines[i]).days >= date_interval[period]
                elif date_interval[period] == 360:
                    assert (klines[i + 1] - klines[i]).days >= date_interval[period]

        def check_date_range(date_result, startDay, endDay):
            # todo 日期范围校验不需要，如果没有数据会补上，优先limit然后是日期范围，不能作为测试依据
            startTS = str_to_stamp(startDay, sep="")
            endTS = str_to_stamp(endDay, sep="")
            kline_records = list(map(lambda x: str_to_stamp(x.split()[0]), date_result))
            for record_ts in kline_records:
                assert startTS <= record_ts <= endTS

    @pytest.mark.parametrize("stock_code,limit,fields,isSubcrible", [
        ('000001.SZ', 10, "$all", "true"),
        ('00001.HK', 200, "$all", "true"),
        ('131800.SZ', 200, "$all", "true"),  # 期权
        ('131800.SZ', 200, "$all", "true"),  # 国债逆回购
        ('123002.SZ', 10, "$all", "true"),  # 可转债
        ('200011.SZ', 10, "$all", "true"),  # 债券（除可转债）
        ('200011.SZ', 10, "$all", "true"),  # B股
        ('159602.SZ', 10, "$all", "true"),  # ETF基金
        ('180201.SZ', 10, "$all", "true"),  # 基金
        ('399481.SZ', 10, "$all", "true"),  # 债券指数
        ('399001.SZ', 10, "$all", "true"),  # 指数
        ('000001.SZ', 10, "$all", "true"),  # 股票
        ('204001.SH', 200, "$all", "true"),  # 国债逆回购
        ('000001.SZ', 10, "deallots", "true"),  # 期权
    ])
    def test_split_the_deal(self, stock_code, limit, fields, isSubcrible):
        """
        1,选择分笔成交
        2,编辑js脚本并执行
        3,校验结果: 长度，字段显示，订阅后数据变化
        """
        self.webSDK.choice_busy_by_txt("分笔成交")
        # 自定义js cmd变量
        cmd = self.webSDK.ticket_js(stock_code=stock_code, limit=limit, fields=fields, isSubcrible=isSubcrible)
        # web端设置自定义的js命令字符串
        self.webSDK.set_js_value(cmd)
        self.webSDK.exec_js_cmd(cmd)
        record = self.webSDK.get_search_result()
        # 3.1 校验长度
        records = record.split("\n")
        assert len(records) <= limit

        # 3.2 校验字段显示
        expect_titles = "time,price,volume,amount,deallots" if fields == "$all" else fields
        real_titles = self.webSDK.get_result_title()
        processed_titles = self.webSDK.process_titles(real_titles)
        assert expect_titles == processed_titles

        # 3.3 校验订阅后字段更新数据，不订阅不更新数据
        time.sleep(6)
        new_record = self.webSDK.get_search_result()
        if isSubcrible:
            assert new_record != records
        else:
            assert new_record == records
