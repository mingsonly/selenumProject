# coding=utf-8
import pytest
import os
import time

def run(file="test_websdk.py"):
    pytest.main(['--alluredir', './reports', file])


if __name__ == '__main__':
    run()
    # path = os.path.dirname(__file__)
    # for _, _, files in os.walk(path):
    #     for file in files:
    #         if file.startswith("test_"):
    #             run(file)
    time.sleep(2)
    # 生成报告
    os.system("allure serve ./reports")
