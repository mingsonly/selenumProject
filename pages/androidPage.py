# coding=utf-8
import time

from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class AndBasePage(BasePage):
    _blacklist = [(By.ID, "com.lbe.security.miui:id/permission_allow_foreground_only_button")]
    # connect按钮
    connect_loc = (By.ID, "com.org.test:id/btn_1")
    connect_userid_loc = (By.ID, "com.org.test:id/connect_userid")
    connect_token_loc = (By.ID, "com.org.test:id/connect_token")
    connect_pro_loc = (By.ID, "com.org.test:id/connect_pro")
    ssl_status_loc = (By.ID, "com.org.test:id/ssl_status")
    loginAppKey_loc = (By.ID, "com.org.test:id/loginAppKey")
    loginAppSecret_loc = (By.ID, "com.org.test:id/loginAppSecret")
    env_EditText_loc = (By.ID, "com.org.test:id/env_EditText")
    connect_cancel_loc = (By.ID, "com.org.test:id/connect_cancel")
    connect_submit_loc = (By.ID, "com.org.test:id/connect_submit")
    # 断开连接
    disconnect_loc = (By.ID, "com.org.test:id/btn_2")
    # 环境导入相关定位
    importenvbtn_loc = (By.ID, "com.org.test:id/btn_33")
    importenvtxt_loc = (By.ID, "com.org.test:id/importenvtext")
    importaccept_loc = (By.ID, "com.org.test:id/importenv_submit")
    importcancel_loc = (By.ID, "com.org.test:id/importenv_cancel")
    # k线数据
    kline_loc = (By.ID, "com.org.test:id/btn_3")
    kline_code_loc = (By.ID, "com.org.test:id/kline_code")
    kline_period_loc = (By.ID, "android:id/text1")
    kline_cqMode_loc = (By.ID, "com.org.test:id/kline_cqMode")
    kline_begin_loc = (By.ID, "com.org.test:id/kline_begin")
    kline_count_loc = (By.ID, "com.org.test:id/kline_count")
    kline_isSub_loc = (By.ID, "com.org.test:id/switchK")
    kline_beginDate_loc = (By.ID, "com.org.test:id/kline_beginDate")
    kline_endDate_loc = (By.ID, "com.org.test:id/kline_endDate")
    kline_cancel_loc = (By.ID, "com.org.test:id/kline_cancel")
    kline_submit_loc = (By.ID, "com.org.test:id/kline_submit")
    # 分时数据
    gtrend_query_loc = (By.ID, "com.org.test:id/gtrend_query")
    gtrend_code_loc = (By.ID, "com.org.test:id/gtrend_code")
    gtrend_days_loc = (By.ID, "com.org.test:id/gtrend_days")
    gtrend_isSub_loc = (By.ID, "com.org.test:id/switchT")
    gtrend_cancel_loc = (By.ID, "com.org.test:id/gtrend_cancel")
    gtrend_submit_loc = (By.ID, "com.org.test:id/gtrend_submit")
    # 历史分时
    hisdata_loc = (By.ID, "com.org.test:id/histrend_query")
    histrend_code_loc = (By.ID, "com.org.test:id/histrend_code")
    histrend_date_loc = (By.ID, "com.org.test:id/histrend_date")
    histrend_cancel_loc = (By.ID, "com.org.test:id/histrend_cancel")
    histrend_submit_loc = (By.ID, "com.org.test:id/histrend_submit")
    # 行情订阅
    mark_loc = (By.ID, "com.org.test:id/btn_6")
    snapshot_code_loc = (By.ID, "com.org.test:id/snapshot_code")
    snapshot_fields_loc = (By.ID, "com.org.test:id/snapshot_fields")
    snapshot_cancel_loc = (By.ID, "com.org.test:id/snapshot_cancel")
    snapshot_submit_loc = (By.ID, "com.org.test:id/snapshot_submit")
    # 集合竞价
    callaution_query_loc = (By.ID, "com.org.test:id/callaution_query")
    callaution_code_loc = (By.ID, "com.org.test:id/callaution_code")
    callaution_field_loc = (By.ID, "com.org.test:id/callaution_field")
    switchCallauton_loc = (By.ID, "com.org.test:id/switchCallauton")
    callaution_cancel_loc = (By.ID, "com.org.test:id/callaution_cancel")
    callaution_submit_loc = (By.ID, "com.org.test:id/callaution_submit")
    # 分笔成交
    gtick_query_loc = (By.ID, "com.org.test:id/gtick_query")
    gtick_code_loc = (By.ID, "com.org.test:id/gtick_code")
    gtick_begin_loc = (By.ID, "com.org.test:id/gtick_begin")
    gtick_count_loc = (By.ID, "com.org.test:id/gtick_count")
    gtick_field_loc = (By.ID, "com.org.test:id/gtick_field")
    switchTick_loc = (By.ID, "com.org.test:id/switchTick")
    gtick_cancel_loc = (By.ID, "com.org.test:id/gtick_cancel")
    gtick_submit_loc = (By.ID, "com.org.test:id/gtick_submit")
    # 涨跌家数
    updowns_query_loc = (By.ID, "com.org.test:id/updowns_query")
    updown_code_loc = (By.ID, "com.org.test:id/updown_code")
    updown_cancel_loc = (By.ID, "com.org.test:id/updown_cancel")
    updown_submit_loc = (By.ID, "com.org.test:id/updown_submit")
    # 板块排序
    sort_query_loc = (By.ID, "com.org.test:id/sort_query")
    sort_sectorid_loc = (By.ID, "com.org.test:id/sort_sectorid")
    sort_codes_loc = (By.ID, "com.org.test:id/sort_codes")
    sort_fields_loc = (By.ID, "com.org.test:id/sort_fields")
    asc_or_desc_loc = (By.ID, "android:id/text1")
    sort_begin_loc = (By.ID, "com.org.test:id/sort_begin")
    sort_count_loc = (By.ID, "com.org.test:id/sort_count")
    sort_cancel_loc = (By.ID, "com.org.test:id/sort_cancel")
    sort_submit_loc = (By.ID, "com.org.test:id/sort_submit")
    # 分价统计
    priceStatit_loc = (By.ID, "com.org.test:id/priceStati")
    pricestatic_code_loc = (By.ID, "com.org.test:id/pricestatic_code")
    pricestatic_begin_loc = (By.ID, "com.org.test:id/pricestatic_begin")
    pricestatic_count_loc = (By.ID, "com.org.test:id/pricestatic_count")
    switchP_loc = (By.ID, "com.org.test:id/switchP")
    pricestatic_cancel_loc = (By.ID, "com.org.test:id/pricestatic_cancel")
    pricestatic_submit_loc = (By.ID, "com.org.test:id/pricestatic_submit")

    def __init__(self, webdriver):
        super().__init__(webdriver)

    def impower(self):
        for loc in self._blacklist:
            if self.get_element(loc):
                self.click(loc)

    def connect_server(self, userid, token, loginAppKey, appSecret, pro_env='dev', env='uat', isConnect='submit',
                       openSSL=None):
        self.click(self.connect_loc)
        self.input_text(userid, self.connect_userid_loc)
        self.input_text(token, self.connect_token_loc)
        if openSSL:
            self.click(self.ssl_status_loc)
        self.input_text(pro_env, self.connect_pro_loc)
        self.input_text(loginAppKey, self.loginAppKey_loc)
        self.input_text(appSecret, self.loginAppSecret_loc)
        self.input_text(env, self.env_EditText_loc)
        connect_status = {
            "submit": self.connect_submit_loc,
            "cancel": self.connect_cancel_loc,
        }
        self.click(connect_status[isConnect])

    def envs_import_busy(self, envs, busy='import_accept'):
        busy_type = {
            "import_accept": self.importaccept_loc,  # 确认按钮
            "abort_import": self.importaccept_loc,  # 取消按钮
        }
        """环境导入：点击导入按钮"""
        self.click(loc=self.importenvbtn_loc)
        """环境导入：导入环境配置"""
        self.input_text(text=envs, loc=self.importenvtxt_loc)

        """环境导入：点击确定 or取消  按钮"""
        self.click(busy_type[busy])
