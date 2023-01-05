# encoding: utf-8
# __author:  angel
# date:  2022/12/24
from util.common import get_android_devices, get_logger
from util.shell import Shell, ADB
from util.config import Config

import yaml

log = get_logger()


class EnvironmentInfo(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!EnvironmentInfo'

    def __init__(self, appium, devices, apk, pages_yaml, xml_report, html_report, app_activity, app_package):
        self.appium = appium
        self.devices = devices
        self.apk = apk
        self.pages_yaml = pages_yaml
        self.xml_report = xml_report
        self.html_report = html_report
        self.app_activity = app_activity
        self.app_package = app_package


class DeviceInfo(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!DeviceInfo'

    def __init__(self, device_name, platform_name, platform_version):
        self.device_name = device_name
        self.platform_name = platform_name
        self.platform_version = platform_version


class Environment:

    def __init__(self):
        self.devices = get_android_devices()
        self.appium_version = Shell.start("appium -v").splitlines()[0].strip()
        self.config = Config()
        self.check_environment()
        self.save_environment()

    def check_environment(self):
        log.info("检查环境...")
        # 检查appium版本
        if '1.22' not in self.appium_version:
            log.error("appium 版本不对")
            exit()
        else:
            log.info("appium version {}".format(self.appium_version))
        # 检查设备是否在线
        if not self.devices:
            log.error("设备不在线")
            exit()
        else:
            log.info("已连接设备: ", self.devices)

    def save_environment(self):
        infos = []
        env_path = self.config.env_yaml_path
        apk_path = self.config.apk_path
        pages_yaml_path = self.config.pages_yaml_path
        xml_yaml_path = self.config.xml_report_path
        html_yaml_path = self.config.html_report_path
        app_activity = self.config.app_activity
        app_package = self.config.app_package
        for device in self.devices:
            info = DeviceInfo(device, "Android", ADB(device).get_android_version())
            infos.append(info)
        env_info = EnvironmentInfo(self.appium_version, infos, apk_path, pages_yaml_path, xml_yaml_path, html_yaml_path,
                                   app_activity, app_package)
        with open(env_path, "w") as f:
            yaml.dump(env_info, f, default_flow_style=False)
        log.info("保存环境配置 path: " + env_path)

    def get_environment_info(self):
        env_path = self.config.env_yaml_path
        with open(env_path, 'r') as f:
            env_info = yaml.safe_load(f)
        return env_info

    def get_inited_config(self):
        return self.config

# if __name__ == '__main__':
#     env = Environment()
#     env.check_environment()
#     env.check_environment()
#     print(env.get_environment_info())