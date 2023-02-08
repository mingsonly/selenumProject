# encoding: utf-8
import time
import allure
from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from util.common import get_logger

log = get_logger()


@allure.story("websdk登录")
class WebSDKPage(BasePage):
    url = "https://uat-cloud.hongwuniu.com/page/gsdk/demo/index.html"
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
    title_loc = (By.XPATH, '//*[@id="showTable"]/thead/tr')
    result_loc = (By.XPATH, '//*[@id="showTable"]/tbody')
    busy_type = (By.XPATH, '//*[@id="funcSelect"]')
    js_loc = (By.XPATH, '//*[@id="editor"]/div[2]/div')
    func_str = """
            function onCallback (response){
                //结果集
                GTSEvent.event(DataEvent.ACCEPTDATA,response);
            }
            """

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

    @allure.step("选择业务类型（下标）")
    def choice_busy_by_index(self, index):
        select = self.get_select_obj(self.busy_type)
        select.select_by_index(index)

    @allure.step("选择业务类型（文本）")
    def choice_busy_by_txt(self, txt):
        select = self.get_select_obj(self.busy_type)
        select.select_by_visible_text(txt)

    @allure.step("登录")
    def login(self):
        self.click(self.login_loc)

    @allure.step("关闭浏览器")
    def close(self):
        self.quit()

    @allure.step("执行js命令")
    def exec_js_cmd(self, cmd):
        self.exex_js(cmd)

    @allure.step("设置JS命令")
    def set_js_value(self, cmd):
        self.exex_js(f"editor.setValue(`{cmd}`)")

    @allure.step("获取JS命令")
    def get_js_value(self):
        self.exex_js("editor.getValue()")

    @allure.step("处理查询结果集合字段（转小写-->空格替换成逗号）")
    def process_titles(self, titles):
        # 转小写并空格替换成逗号
        lower_titles = titles.lower()
        processed_titles = lower_titles.replace(" ", ",")
        return processed_titles

    def search_key_js(self, page_no, page_size, keyword, fields="sufSecuCode,secuAbbr",
                      category="SDK_KEYWIZARD_CATEGORY_ALL", market="SDK_KEYWIZARD_MARKET_SHSZHK"):
        cmd = self.func_str + """
            let searchKeyword = NSDK.createRequestItem(SDK_REQUEST_KEYWIZARD);
            searchKeyword.setDataCallback(onCallback);""" + f"""
            searchKeyword.setCategory({category});""" + f"""
            searchKeyword.setMarket({market});""" + f"""
            searchKeyword.setFields("{fields}");""" + f"""
            searchKeyword.setPageNo({page_no});
            searchKeyword.setPageSize({page_size});
            searchKeyword.match("{str(keyword)}");
        """
        return cmd

    def get_search_result(self):
        try:
            keyword_text = self.get_element(self.result_loc).text
        except ValueError:
            log.log("查询结果为空，请稍后，正在重新请求！！！")
            keyword_text = self.get_element(self.result_loc).text
        return keyword_text

    def get_result_title(self):
        try:
            title = self.get_element(self.title_loc).text
        except ValueError:
            log.log("结果标题为空，请稍后，正在重新请求！！！")
            title = self.get_element(self.title_loc).text
        return title

    def singel_stock_js(self, stocks: str, fields="Code,Name,SectorID,SectorName,MarginTrade,StockConnect"):
        """个股信息"""
        cmd = self.func_str + """
            let stockInformation = NSDK.createRequestItem(SDK_REQUEST_NSTOCKINFO);
            stockInformation.setDataCallback(onCallback);""" + f"""
            stockInformation.setCodes("{stocks}");
            stockInformation.setFields("{fields}");
            stockInformation.request();
        """
        return cmd

    def snapshotUpdowns_js(self, stock_code):
        """涨价跌数"""
        snap_cmd = self.func_str + """
        let snapshotUpdowns = NSDK.createRequestItem(SDK_REQUEST_UPDOWNDISTRIBUTION);
        //设置回调函数
        snapshotUpdowns.setDataCallback(onCallback);""" + f"""
        snapshotUpdowns.setCode("{stock_code}");
        //开始查询
        snapshotUpdowns.request();
        """
        return snap_cmd

    def kLine_js(self, stock_code="600000.SH", period="SDK_KLINE_PERIOD_DAY", cqMode="SDK_KLINE_CQMODE_FORWARD",
                 orderType=-1, startDay="20201124", endDay="20210315", fields="$all",
                 isSubcrible="true", size=10):
        """K线数据"""
        kline_cmd = self.func_str + """
            let kLine = NSDK.createRequestItem(SDK_REQUEST_KLINE);
            kLine.setDataCallback(onCallback);
        """ + f"""
            kLine.setCode("{stock_code}");
            kLine.setPeriod({str(period)});
            kLine.setCqMode({str(cqMode)});
            kLine.setLimit({orderType},{size});
            kLine.setDateRange("{startDay}","{endDay}");
            kLine.setFields("{fields}");
            kLine.setSubscribe({isSubcrible});
            //开始查询
            kLine.request();
        """
        return kline_cmd

    def order_js(self, stock_code="000001.SZ", limit=10, fields="all", isSubcrible=True):
        """逐笔委托"""
        order_cmd = self.func_str + """
            let order  = NSDK.createRequestItem(SDK_REQUEST_ORDER);
            //设置回调函数
            order.setDataCallback(onCallback);
        """ + f"""
            order.setCode("{stock_code}");
            order.setLimit(-1,{limit});
            order.setFields("${fields}");
            order.setSubscribe({isSubcrible});
            //开始查询
            order.request();
        """
        return order_cmd

    def step_order_js(self, stock_code='000001.SZ', limit=10, fields="$all", isWithdrawal="false", isSubcrible=True):
        """逐笔成交"""
        step_cmd = self.func_str + """
            let step  = NSDK.createRequestItem(SDK_REQUEST_STEP);
            //设置回调函数
            step.setDataCallback(onCallback);
        """ + f"""
            step.setCode("{stock_code}");
            step.setWithdrawal({isWithdrawal});
            step.setLimit(-1,{limit});
            step.setFields("{fields}");
            step.setSubscribe({isSubcrible});
            //开始查询
            step.request();
        """
        return step_cmd

    def ticket_js(self, stock_code='000001.SZ', limit=10, fields="$all", isSubcrible="true"):
        "分笔成交"
        step_cmd = self.func_str + """
            let tick  = NSDK.createRequestItem(SDK_REQUEST_TICK);
            //设置回调函数
            tick.setDataCallback(onCallback);""" + f"""
            tick.setCode("{stock_code}");
            tick.setLimit(-1,{limit});
            tick.setFields("{fields}");
            tick.setSubscribe({isSubcrible});
            //开始查询
            tick.request();
        """
        return step_cmd

    def sort_js(self, stock_code='000001.SZ,600000.SH,688588.SH', limit=10, sortedFields="PercentChange"):
        """板块排序"""
        sort_cmd = self.func_str + """
            let sort = NSDK.createRequestItem(SDK_REQUEST_SORT);
            //设置回调函数
            sort.setDataCallback(onCallback);""" + f"""
            sort.setCodes("{stock_code}");
            sort.setSectorId("101010199911000");
            sort.setSortField("{sortedFields}",SDK_SORTTYPE_DESC);
            sort.setLimit(-1,{limit});
            //开始查询
            sort.request();
        """
        return sort_cmd

    def trend_js(self, stock_code='000001.SZ', days=1, fields="all", subcrible="true"):
        """分时数据"""
        trend_cmd = self.func_str + f"""
            let trend  = NSDK.createRequestItem(SDK_REQUEST_TREND);
            //设置回调函数
            trend.setDataCallback(onCallback);
            trend.setCode("{stock_code}");
            trend.setDays({days});
            trend.setFields("${fields}");
            trend.setSubscribe({subcrible});
            //开始查询
            trend.request();
        """
        return trend_cmd

    def hisTrend_js(self, stock_code='000001.SZ', date="20210524", fields="all"):
        """历史分时"""
        hisTrend_cmd = self.func_str + f"""
            let hisTrend  = NSDK.createRequestItem(SDK_REQUEST_HISTREND);
            //设置回调函数
            hisTrend.setDataCallback(onCallback);
            hisTrend.setCode("{stock_code}");
            hisTrend.setDate("{date}");
            hisTrend.setFields("${fields}");
            //开始查询
            hisTrend.request();
        """
        return hisTrend_cmd

    def callAution_js(self, stock_code='000001.SZ', fields="all", subcrible=True):
        """集合竞价"""
        callAution_cmd = self.func_str + f"""
            let callAution  = NSDK.createRequestItem(SDK_REQUEST_CALLAUTION);
            //设置回调函数
            callAution.setDataCallback(onCallback);
            callAution.setCode("{stock_code}");
            callAution.setFields("${fields}");
            callAution.setSubscribe({subcrible});
            //开始查询
            callAution.request();
        """
        return callAution_cmd

    def subscribe_js(self, stock_code='000001.SZ,000002.SZ', fields="code,last,change"):
        """行情订阅"""
        subscribe_cmd = self.func_str + f"""
            let subscribe   = NSDK.createRequestItem(SDK_REQUEST_QUOTESUBSCRIBE);
            //设置回调函数
            subscribe.setDataCallback(onCallback);
            subscribe.setCodes("{stock_code}");
            subscribe.setFields("{fields}");
            //开始查询
            subscribe.request();
        """
        return subscribe_cmd

    def price_js(self, stock_code='000001.SZ,000002.SZ', limit=10, fields="all", subcrible=True):
        """分价统计"""
        price_cmd = self.func_str + f"""
            let price   = NSDK.createRequestItem(SDK_REQUEST_PRICEDISTRIBUTION);
            //设置回调函数
            price.setDataCallback(onCallback);
            price.setCode("{stock_code}");
            price.setLimit(-1,{limit});
            price.setFields("${fields}");
            price.setSubscribe({subcrible});
            //开始查询
            price.request();
        """
        return price_cmd

    def select_plate_js(self):
        """查询板块"""
        sel_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_GET);
            requestCommon.setParam(SDK_USERSECTOR_USERID,"{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_FIELDS,SDK_USERSECTOR_FIELDS_VALUE);
            //开始查询
            requestCommon.request();
        """
        return sel_plate_cmd

    def add_plate_js(self, plate_name):
        """添加板块"""
        add_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_ADD);
            requestCommon.setParam(SDK_USERSECTOR_FIELDS,"sectorid");
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORNAME,'{plate_name}');//添加的板块名称
            //开始查询
            requestCommon.request();
        """
        return add_plate_cmd

    def del_plate_js(self, plate_id='1537874208340045824'):
        """删除板块"""
        del_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_DELETE);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//删除的板块id
            //开始查询
            requestCommon.request();
        """
        return del_plate_cmd

    def rename_plate_js(self, new_name, plate_id='1537874208340045824'):
        """修改板块名称"""
        rename_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_EDIT);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//板块id
            requestCommon.setParam(SDK_USERSECTOR_SECTORNAME, '{new_name}');
            //开始查询
            requestCommon.request();
        """
        return rename_plate_cmd

    def move_plate_js(self, index=0, plate_id='1537874208340045824'):
        """移动板块位置"""
        move_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_MOVE);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//移动的板块
            requestCommon.setParam(SDK_USERSECTOR_TARGETINDEX, {index});//移动到的下标 0开始
            //开始查询
            requestCommon.request();
        """
        return move_plate_cmd

    def search_mystock_js(self, plate_id='1537874208340045824', fields='secucode'):
        """查询自选股"""
        search_mystock_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECURITY_GET);
            requestCommon.setParam(SDK_USERSECURITY_USERID,"{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECURITY_SECTORID,"{plate_id}");//被查询板块的id
            requestCommon.setParam("fields","{fields}");//查询字段
            //开始查询
            requestCommon.request();
        """
        return search_mystock_cmd

    def add_mystock_js(self, plate_id='1537874208340045824', stock='600000.SH'):
        """添加自选股"""
        add_mystock_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            requestCommon.setDataCallback(onCallback);
            //设置回调函数
            requestCommon.setAPI(SDK_USERSECURITY_ADD);
            requestCommon.setParam(SDK_USERSECURITY_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECURITY_SECTORID, "{plate_id}");//添加股票的板块id
            requestCommon.setParam(SDK_USERSECURITY_SECURITYS, "{stock}");//添加的股票代码
            //开始查询
            requestCommon.request();
        """
        return add_mystock_cmd
