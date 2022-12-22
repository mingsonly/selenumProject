# coding=utf-8
import time

from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class AndBasePage(BasePage):
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

    def disconnect(self):
        self.click(self.disconnect_loc)

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

    # 板块成分
    sectorplate_loc = (By.ID, "com.org.test:id/sectorplate")
    sectorplate_id_loc = (By.ID, "com.org.test:id/sectorplate_id")
    sectorplate_begin_loc = (By.ID, "com.org.test:id/sectorplate_begin")
    sectorplate_count_loc = (By.ID, "com.org.test:id/sectorplate_count")
    sectorplate_cancel_loc = (By.ID, "com.org.test:id/sectorplate_cancel")
    sectorplate_submit_loc = (By.ID, "com.org.test:id/sectorplate_submit")

    # 指数对应板块
    indexForId_loc = (By.ID, "com.org.test:id/indexForId")
    indexforid_id_loc = (By.ID, "com.org.test:id/indexforid_id")
    indexforid_cancel_loc = (By.ID, "com.org.test:id/indexforid_cancel")
    indexforid_submit_loc = (By.ID, "com.org.test:id/indexforid_submit")

    # 逐笔成交
    gStep_loc = (By.ID, "com.org.test:id/gStep")
    gstep_code_loc = (By.ID, "com.org.test:id/gstep_code")
    gstep_begin_loc = (By.ID, "com.org.test:id/gstep_begin")
    gstep_count_loc = (By.ID, "com.org.test:id/gstep_count")
    gstep_field_loc = (By.ID, "com.org.test:id/gstep_field")
    switchStep_loc = (By.ID, "com.org.test:id/switchStep")
    withdrawal_loc = (By.ID, "com.org.test:id/withdrawal")
    gstep_cancel_loc = (By.ID, "com.org.test:id/gstep_cancel")
    gstep_submit_loc = (By.ID, "com.org.test:id/gstep_submit")

    # 逐笔委托
    gOrder_loc = (By.ID, "com.org.test:id/gOrder")
    gorder_code_loc = (By.ID, "com.org.test:id/gorder_code")
    gorder_begin_loc = (By.ID, "com.org.test:id/gorder_begin")
    gorder_count_loc = (By.ID, "com.org.test:id/gorder_count")
    gorder_field_loc = (By.ID, "com.org.test:id/gorder_field")
    switchOrder_loc = (By.ID, "com.org.test:id/switchOrder")
    gorder_cancel_loc = (By.ID, "com.org.test:id/gorder_cancel")
    gorder_submit_loc = (By.ID, "com.org.test:id/gorder_submit")

    # 买卖队列
    gTradeQueue_loc = (By.ID, "com.org.test:id/gTradeQueue")
    gtrade_code_loc = (By.ID, "com.org.test:id/gtrade_code")
    gtrade_type_loc = (By.ID, "com.org.test:id/gtrade_type")
    gtrade_cancel_loc = (By.ID, "com.org.test:id/gtrade_cancel")
    gtrade_submit_loc = (By.ID, "com.org.test:id/gtrade_submit")

    # 分量统计
    gVolumeStatistics_loc = (By.ID, "com.org.test:id/gVolumeStatistics")
    gvolume_code_loc = (By.ID, "com.org.test:id/gvolume_code")
    gvolume_cancel_loc = (By.ID, "com.org.test:id/gvolume_cancel")
    gvolume_submit_loc = (By.ID, "com.org.test:id/gvolume_submit")

    # 资金流向
    gMoneyFlow_loc = (By.ID, "com.org.test:id/gMoneyFlow")
    gmoney_code_loc = (By.ID, "com.org.test:id/gmoney_code")
    gmoney_cancel_loc = (By.ID, "com.org.test:id/gmoney_cancel")
    gmoney_submit_loc = (By.ID, "com.org.test:id/gmoney_submit")

    # 定制开发
    quoteTest_loc = (By.ID, "com.org.test:id/quoteTest")
    quote_interface_loc = (By.ID, "com.org.test:id/quote_interface")
    quote_field_loc = (By.ID, "com.org.test:id/quote_field")
    quote_condition_loc = (By.ID, "com.org.test:id/quote_condition")
    quote_keys_loc = (By.ID, "com.org.test:id/quote_keys")
    quote_range_loc = (By.ID, "com.org.test:id/quote_range")
    quote_subscribe_loc = (By.ID, "com.org.test:id/quote_subscribe")
    quote_cancel_loc = (By.ID, "com.org.test:id/quote_cancel")
    quote_submit_loc = (By.ID, "com.org.test:id/quote_submit")

    # 个股信息
    nStockInfo_loc = (By.ID, "com.org.test:id/nStockInfo")
    nstockinfo_codes_loc = (By.ID, "com.org.test:id/nstockinfo_codes")
    nstockinfo_fields_loc = (By.ID, "com.org.test:id/nstockinfo_fields")
    nstockinfo_cancel_loc = (By.ID, "com.org.test:id/nstockinfo_cancel")
    nstockinfo_submit_loc = (By.ID, "com.org.test:id/nstockinfo_submit")

    # 键盘精灵
    btn_5_loc = (By.ID, "com.org.test:id/btn_5")
    keyWizard_code_loc = (By.ID, "com.org.test:id/keyWizard_code")
    keyWizard_category_loc = (By.ID, "com.org.test:id/keyWizard_category")
    kline_market_loc = (By.ID, "com.org.test:id/kline_market")
    keyWizard_begin_loc = (By.ID, "com.org.test:id/keyWizard_begin")
    keyWizard_count_loc = (By.ID, "com.org.test:id/keyWizard_count")
    keyWizard_field_loc = (By.ID, "com.org.test:id/keyWizard_field")
    keyWizard_cancel_loc = (By.ID, "com.org.test:id/keyWizard_cancel")
    keyWizard_submit_loc = (By.ID, "com.org.test:id/keyWizard_submit")

    def keyWizard_query_all(self, code, category, market, begin, count, field=None, isQuery=True):
        self.click(self.btn_5_loc)
        self.input_text(code, self.keyWizard_code_loc)
        self.input_text(category, self.keyWizard_category_loc)
        self.input_text(market, self.kline_market_loc)
        self.input_text(begin, self.keyWizard_begin_loc)
        self.input_text(count, self.keyWizard_count_loc)
        if field:
            self.input_text(field, self.keyWizard_field_loc)

        if isQuery:
            self.click(self.keyWizard_submit_loc)
        else:
            self.click(self.keyWizard_cancel_loc)

    # 自选股板块操作
    # 查询板块
    sector_query_loc = (By.ID, "com.org.test:id/sector_query")
    sector_query_name_loc = (By.XPATH, "//*[contains(@resource-id,'com.org.test:id/lv_two_2')]")
    sector_query_id_loc = (By.XPATH, "//*[contains(@resource-id,'com.org.test:id/lv_two_1')]")
    phone_permission_loc = (By.XPATH, "//*[contains(@text,'允许') and contains(@resource-id, 'android:id/button1')]")

    # 添加板块
    sector_add_loc = (By.ID, "com.org.test:id/sector_add")
    sector_add_name_loc = (By.ID, "com.org.test:id/sector_add_name")
    sector_add_cancel_loc = (By.ID, "com.org.test:id/sector_add_cancel")
    sector_add_submit_loc = (By.ID, "com.org.test:id/sector_add_submit")

    # 删除板块
    sector_delete_loc = (By.ID, "com.org.test:id/sector_delete")
    sector_delete_id_loc = (By.ID, "com.org.test:id/sector_delete_id")
    sector_delete_cancel_loc = (By.ID, "com.org.test:id/sector_delete_cancel")
    sector_delete_submit_loc = (By.ID, "com.org.test:id/sector_delete_submit")

    # 修改板块
    sector_update_loc = (By.ID, "com.org.test:id/sector_update")
    sector_update_id_loc = (By.ID, "com.org.test:id/sector_update_id")
    sector_update_name_loc = (By.ID, "com.org.test:id/sector_update_name")
    sector_update_cancel_loc = (By.ID, "com.org.test:id/sector_update_cancel")
    sector_update_submit_loc = (By.ID, "com.org.test:id/sector_update_submit")

    # 移动板块
    sector_sort_loc = (By.ID, "com.org.test:id/sector_sort")
    sector_sort_id_loc = (By.ID, "com.org.test:id/sector_sort_id")
    sector_sort_index_loc = (By.ID, "com.org.test:id/sector_sort_index")
    sector_sort_cancel_loc = (By.ID, "com.org.test:id/sector_sort_cancel")
    sector_sort_submit_loc = (By.ID, "com.org.test:id/sector_sort_submit")

    def phone_permission_enable(self):
        self.wait_util_click(self.phone_permission_loc)

    def sector_move(self, sector_id, index, isMvoe=True):
        """板块移动"""
        self.click(self.sector_sort_loc)
        self.input_text(sector_id, self.sector_sort_id_loc)
        self.input_text(index, self.sector_sort_index_loc)
        if isMvoe:
            self.click(self.sector_sort_submit_loc)
        else:
            self.click(self.sector_sort_cancel_loc)

    def sector_update(self, sector_id, sector_name, isUp=True):
        """板块更新"""
        self.click(self.sector_update_loc)
        self.input_text(sector_id, self.sector_update_id_loc)
        self.input_text(sector_name, self.sector_update_name_loc)
        if isUp:
            self.click(self.sector_update_submit_loc)
        else:
            self.click(self.sector_update_cancel_loc)

    def sector_delete(self, sector_id, isDel=True):
        # 删除板块
        self.click(self.sector_delete_loc)
        self.input_text(sector_id, self.sector_delete_id_loc)
        if isDel:
            self.click(self.sector_delete_submit_loc)
        else:
            self.click(self.sector_delete_submit_loc)

    def sector_query(self):
        # 查询板块
        self.click(self.sector_query_loc)
        result = self.get_result()
        return result

    def get_result(self):
        names = self.get_elements(self.sector_query_name_loc)
        ids = self.get_elements(self.sector_query_id_loc)
        sectors = dict()
        for name, id in zip(names, ids):
            sectors[name.text] = id.text
        return sectors

    def sector_add(self, sector_name, isAdd=True):
        "添加板块"
        self.click(self.sector_add_loc)
        self.input_text(sector_name, self.sector_add_name_loc)
        if isAdd:
            self.click(self.sector_add_submit_loc)
        else:
            self.click(self.sector_add_cancel_loc)

    #

    # =========================自选股操作===============================
    # 查询自选股
    securitys_query_loc = (By.ID, "com.org.test:id/securitys_query")
    securitys_query_id_loc = (By.ID, "com.org.test:id/securitys_query_id")
    securitys_query_cancel_loc = (By.ID, "com.org.test:id/securitys_query_cancel")
    securitys_query_submit_loc = (By.ID, "com.org.test:id/securitys_query_submit")
    # 添加自选股
    securitys_add_loc = (By.ID, "com.org.test:id/securitys_add")
    securitys_add_id_loc = (By.ID, "com.org.test:id/securitys_add_id")
    securitys_add_code_loc = (By.ID, "com.org.test:id/securitys_add_code")
    securitys_add_cancel_loc = (By.ID, "com.org.test:id/securitys_add_cancel")
    securitys_add_submit_loc = (By.ID, "com.org.test:id/securitys_add_submit")

    # 删除自选股
    securitys_delete_loc = (By.ID, "com.org.test:id/securitys_delete")
    securitys_delete_id_loc = (By.ID, "com.org.test:id/securitys_delete_id")
    securitys_delete_code_loc = (By.ID, "com.org.test:id/securitys_delete_code")
    securitys_delete_cancel_loc = (By.ID, "com.org.test:id/securitys_delete_cancel")
    securitys_delete_submit_loc = (By.ID, "com.org.test:id/securitys_delete_submit")
    # 清空自选股
    securitys_clean_loc = (By.ID, "com.org.test:id/securitys_clean")
    securitys_clean_id_loc = (By.ID, "com.org.test:id/securitys_clean_id")
    securitys_clean_cancel_loc = (By.ID, "com.org.test:id/securitys_clean_cancel")
    securitys_clean_submit_loc = (By.ID, "com.org.test:id/securitys_clean_submit")

    # 自选股调整位置
    securitys_sort_loc = (By.ID, "com.org.test:id/securitys_sort")
    securitys_sort_id_loc = (By.ID, "com.org.test:id/securitys_sort_id")
    securitys_sort_code_loc = (By.ID, "com.org.test:id/securitys_sort_code")
    securitys_sort_index_loc = (By.ID, "com.org.test:id/securitys_sort_index")
    securitys_sort_cancel_loc = (By.ID, "com.org.test:id/securitys_sort_cancel")
    securitys_sort_submit_loc = (By.ID, "com.org.test:id/securitys_sort_submit")

    def owner_stock_query(self, sector_id, isQuery=True):
        """
        查询自选股
        :return:
        """
        self.click(self.securitys_query_loc)
        self.input_text(sector_id, self.securitys_query_id_loc)
        add_type = self.securitys_query_submit_loc if isQuery else self.securitys_query_cancel_loc
        self.click(add_type)
        result = self.get_result()
        return result

    def owner_stock_add(self, sector_id, stock_code, isAdd=True):
        """
        添加自选股
        :return:
        """
        # todo 这里需要滚动下拉条，有问题待调试
        self.scroll_web(self.securitys_add_loc)
        self.click(self.securitys_add_loc)
        self.input_text(sector_id, self.securitys_add_id_loc)
        self.input_text(stock_code, self.securitys_add_code_loc)
        add_type = self.securitys_add_submit_loc if isAdd else self.securitys_add_cancel_loc
        self.click(add_type)

    def owner_stock_del(self, sector_id, stock_code, isDel=True):
        """
        删除自选股
        :return:
        """
        self.click(self.securitys_delete_loc)
        self.input_text(sector_id, self.securitys_delete_id_loc)
        self.input_text(stock_code, self.securitys_delete_code_loc)
        add_type = self.securitys_delete_submit_loc if isDel else self.securitys_delete_cancel_loc
        self.click(add_type)

    def owner_stock_clear(self, sector_id, isClear=True):
        """
        清除自选股
        :return:
        """
        self.click(self.securitys_clean_loc)
        self.input_text(sector_id, self.securitys_clean_id_loc)
        clear_type = self.securitys_clean_submit_loc if isClear else self.securitys_clean_cancel_loc
        self.click(clear_type)

    def owner_stock_move(self, sector_id, move_idx, isMove=True):
        """
        移动自选股
        :return:
        """
        self.click(self.securitys_sort_loc)
        self.input_text(sector_id, self.securitys_sort_id_loc)
        self.input_text(move_idx, self.securitys_sort_index_loc)
        add_type = self.securitys_sort_submit_loc if isMove else self.securitys_sort_cancel_loc
        self.click(add_type)

    def __init__(self, webdriver):
        super().__init__(webdriver)

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
