# encoding: utf-8
# __author:  angel
# date:  2022/12/24

import os
from configparser import ConfigParser
from util.common import get_logger

log = get_logger()
class Config:
    default_config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/config.ini"))
    base_path_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # titles
    title_apkInfo = 'apkInfo'
    title_account = 'account'
    # value
    # value-apkInfo
    value_apkName = 'apk'
    value_apkActivity = 'app_activity'
    value_appPackage = 'app_activity'
    # value-account
    value_accoutUser = 'user'
    value_accoutSecret = 'secret'

    def __init__(self):
        self.path = Config.default_config_dir
        self.cp = ConfigParser()
        self.cp.read(self.path)
        log.info("初始化config ...config path: " + self.path)
        apk_name = self.get_config(Config.title_apkInfo, Config.value_apkName)
        self.apk_path = Config.base_path_dir + "/apk/" + apk_name
        self.xml_report_path = Config.base_path_dir + '/report/xml'
        self.html_report_path = Config.base_path_dir + '/report/html'
        self.pages_yaml_path = Config.base_path_dir + '/page/yaml'
        self.env_yaml_path = Config.base_path_dir+'/data/environment_info.yaml'
        self.app_activity = self.get_config(Config.title_apkInfo,Config.value_apkActivity)
        self.app_package = self.get_config(Config.title_apkInfo,Config.value_appPackage)
        self.user = self.get_config(Config.title_account,Config.value_accoutUser)
        self.secret = self.get_config(Config.title_account,Config.value_accoutSecret)

    def set_config(self, titile, value, text):
        self.cp.set(titile, value, text)
        with open(self.path, "w+") as f:
            return self.cp.write(f)

    def add_config(self, title):
        self.cp.add_section(title)
        with open(self.path, "w+") as f:
            return self.cp.write(f)

    def get_config(self, title, value):
        return self.cp.get(title, value)
