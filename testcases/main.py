import pytest
import os
import time

from util.environment import Environment
from util.shell import Shell
from util.common import get_logger

log = get_logger()


def run():
    env = Environment()
    xml_report_path = env.get_environment_info().xml_report
    html_report_path = env.get_environment_info().html_report
    # test
    args = ['-s', '-q', '--alluredir', xml_report_path]
    pytest.main(args)
    # 生成报告
    cmd = "allure generate %s -o %s" % (xml_report_path, html_report_path)
    try:
        Shell.start(cmd)
    except:
        log.error("Html报告生成失败，确定已经安装了Allure-Commandline")


if __name__ == '__main__':
    run()
    # path = os.path.dirname(__file__)
    # for _, _, files in os.walk(path):
    #     for file in files:
    #         if file.startswith("test_"):
    #             run(file)
    # os.system("allure serve ../reports")
