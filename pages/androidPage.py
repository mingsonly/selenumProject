#coding=utf-8
from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class AndBasePage(BasePage):
    connect_loc = (By.ID, "com.org.test:id/btn_1")
    disconnect_loc = (By.ID, "com.org.test:id/btn_2")

    # 环境导入相关定位
    importenvbtn_loc = (By.ID, "com.org.test:id/btn_33")
    importenvtxt_loc = (By.ID, "com.org.test:id/importenvtext")
    importaccept_loc = (By.ID, "com.org.test:id/importenv_submit")
    importcancel_loc = (By.ID, "com.org.test:id/importenv_cancel")


    kline_loc = (By.ID, "com.org.test:id/btn_3")
    mindata_loc = (By.ID, "com.org.test:id/gtrend_query")
    hisdata_loc = (By.ID, "com.org.test:id/histrend_query")
    marketsub_loc = (By.ID, "com.org.test:id/btn_6")

    def __init__(self, webdriver):
        super().__init__(webdriver)

    def envs_import_btn(self):
        """环境导入：点击导入按钮"""
        self.click(loc=self.importenvbtn_loc)

    def envs_info_input(self, envs):
        """环境导入：导入环境配置"""
        self.input_text(text=envs, loc=self.importenvtxt_loc)

    def envs_btn_accept(self):
        """环境导入：点击确定按钮"""
        self.click(self.importaccept_loc)

    def envs_btn_cancel(self):
        """环境导入：点击确定按钮"""
        self.click(self.importaccept_loc)

